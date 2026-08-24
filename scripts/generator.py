"""
Main orchestrator
"""

import logging
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

from validators import InputValidator
from template_processor import TemplateProcessor
from project_builder import ProjectBuilder
from git_helper import GitHelper
from workflow_generator import WorkflowGenerator
from utils import load_json_config, build_template_variables

logger = logging.getLogger(__name__)

class ProjectGenerator:
    """Main orchestrator"""
    
    def __init__(self, inputs: dict):
        self.inputs = inputs
        self.config = load_json_config('android-config')
        self.temp_dir = None
    
    def generate_project(self) -> Dict[str, Any]:
        """Main generation flow"""
        try:
            logger.info("Validating inputs...")
            validator = InputValidator(self.config)
            is_valid, message = validator.validate_all(self.inputs)
            
            if not is_valid:
                return {'success': False, 'error': message}
            
            # Validate GitHub token
            github_token = self.inputs.get('github_token', '').strip()
            if not github_token:
                logger.error("GitHub token is required")
                return {'success': False, 'error': 'GitHub token is missing or empty'}
            
            self.temp_dir = tempfile.mkdtemp(prefix='android_project_')
            logger.info(f"Temp directory: {self.temp_dir}")
            
            builder = ProjectBuilder(self.temp_dir, self.inputs)
            builder.create_directory_structure()
            
            git = GitHelper(
                token=github_token,
                actor=self.inputs.get('github_actor', 'developer')
            )
            git.config_git()
            
            repo_result = git.create_github_repo(
                repo_name=self.inputs['target_repo'],
                description=self.inputs['app_description']
            )
            
            if not repo_result['success']:
                return {'success': False, 'error': repo_result['error']}
            
            git.clone_repo(
                clone_url=repo_result['repo_clone_url'],
                target_path=self.temp_dir
            )
            
            logger.info("Generating project files...")
            processor = TemplateProcessor()
            
            # Build template variables
            template_vars = build_template_variables(self.inputs, self.config)
            logger.info(f"Template variables prepared: {len(template_vars)} variables loaded")
            
            logger.info("Generating workflows...")
            wf_gen = WorkflowGenerator()
            
            logger.info("Committing and pushing...")
            git.commit_and_push(
                repo_path=self.temp_dir,
                message=f"chore: Initialize Android Project - {self.inputs['project_name']}"
            )
            
            logger.info("Generation completed successfully!")
            
            return {
                'success': True,
                'repo_url': repo_result['repo_url'],
                'project_name': self.inputs['project_name']
            }
        
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}", exc_info=True)
            return {'success': False, 'error': str(e)}
        
        finally:
            if self.temp_dir and Path(self.temp_dir).exists():
                try:
                    shutil.rmtree(self.temp_dir)
                    logger.info("Cleanup completed")
                except Exception as e:
                    logger.warning(f"Cleanup failed: {str(e)}")
