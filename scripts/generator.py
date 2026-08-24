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
    """Main orchestrator for Android project generation"""
    
    def __init__(self, inputs: dict):
        self.inputs = inputs
        self.config = load_json_config('android-config')
        self.temp_dir = None
        self.repo_path = None
    
    def generate_project(self) -> Dict[str, Any]:
        """Main generation flow"""
        try:
            logger.info("="*60)
            logger.info("Starting Android Project Generation...")
            logger.info("="*60)
            
            # Step 1: Validate inputs
            logger.info("\n[Step 1/7] Validating inputs...")
            validator = InputValidator(self.config)
            is_valid, message = validator.validate_all(self.inputs)
            
            if not is_valid:
                logger.error(f"Validation failed: {message}")
                return {'success': False, 'error': message}
            
            logger.info(f"✅ Inputs validated successfully")
            
            # Step 2: Validate GitHub token
            logger.info("\n[Step 2/7] Checking GitHub authentication...")
            github_token = self.inputs.get('github_token', '').strip()
            if not github_token:
                logger.error("GitHub token is required but not provided")
                return {
                    'success': False,
                    'error': 'GitHub token is missing or empty. Please provide GH_TOKEN with a PAT that can create repositories.'
                }
            logger.info(f"✅ GitHub token validated")
            
            # Step 3: Create temp directory and project structure
            logger.info("\n[Step 3/7] Creating project structure...")
            self.temp_dir = tempfile.mkdtemp(prefix='android_project_')
            logger.info(f"Temp directory created: {self.temp_dir}")
            
            builder = ProjectBuilder(self.temp_dir, self.inputs)
            builder.create_directory_structure()
            logger.info(f"✅ Project directory structure created")
            
            # Step 4: Build template variables
            logger.info("\n[Step 4/7] Building template variables...")
            template_vars = build_template_variables(self.inputs, self.config)
            logger.info(f"✅ Template variables prepared ({len(template_vars)} variables)")
            
            # Step 5: GitHub operations - Create repo and push
            logger.info("\n[Step 5/7] Setting up GitHub repository...")
            
            git = GitHelper(
                token=github_token,
                actor=self.inputs.get('github_actor', 'developer')
            )
            git.config_git()
            logger.info(f"Git configured for user: {self.inputs.get('github_actor', 'developer')}")
            
            # Create repository
            logger.info(f"Creating GitHub repository: {self.inputs['target_repo']}")
            repo_result = git.create_github_repo(
                repo_name=self.inputs['target_repo'],
                description=self.inputs['app_description']
            )
            
            if not repo_result['success']:
                logger.error(f"Failed to create repository: {repo_result['error']}")
                return {'success': False, 'error': repo_result['error']}
            
            logger.info(f"✅ Repository created: {repo_result['repo_url']}")
            self.repo_path = repo_result['repo_clone_url']
            
            # Clone repository
            logger.info("Cloning repository...")
            clone_success = git.clone_repo(
                clone_url=repo_result['repo_clone_url'],
                target_path=self.temp_dir
            )
            
            if not clone_success:
                logger.error("Failed to clone repository")
                return {'success': False, 'error': 'Failed to clone repository'}
            
            logger.info(f"✅ Repository cloned successfully")
            
            # Step 6: Render and process templates
            logger.info("\n[Step 6/7] Generating project files from templates...")
            processor = TemplateProcessor()
            
            gradle_dsl = self.inputs.get('gradle_dsl', 'kts')
            logger.info(f"Using Gradle DSL: {gradle_dsl}")
            
            # Process project templates
            processor.process_project_templates(
                output_base_path=self.temp_dir,
                variables=template_vars,
                gradle_dsl=gradle_dsl
            )
            logger.info(f"✅ Project templates generated")
            
            # Generate workflows
            logger.info("Generating CI/CD workflows...")
            wf_gen = WorkflowGenerator()
            workflows_path = Path(self.temp_dir) / '.github' / 'workflows'
            workflows_path.mkdir(parents=True, exist_ok=True)
            processor.process_workflow_templates(
                output_path=str(workflows_path),
                variables=template_vars
            )
            logger.info(f"✅ Workflows generated")
            
            # Step 7: Commit and push
            logger.info("\n[Step 7/7] Committing and pushing changes...")
            push_success = git.commit_and_push(
                repo_path=self.temp_dir,
                message=f"chore: Initialize Android Project - {self.inputs['project_name']}"
            )
            
            if not push_success:
                logger.error("Failed to commit and push changes")
                return {'success': False, 'error': 'Failed to commit and push changes'}
            
            logger.info(f"✅ Changes pushed to repository")
            
            logger.info("\n" + "="*60)
            logger.info("✅ PROJECT GENERATION COMPLETED SUCCESSFULLY!")
            logger.info("="*60)
            logger.info(f"Project: {self.inputs['project_name']}")
            logger.info(f"Repository: {repo_result['repo_url']}")
            logger.info("="*60 + "\n")
            
            return {
                'success': True,
                'repo_url': repo_result['repo_url'],
                'project_name': self.inputs['project_name'],
                'package_name': self.inputs['package_name']
            }
        
        except Exception as e:
            logger.error(f"\n❌ Generation failed with error: {str(e)}", exc_info=True)
            return {'success': False, 'error': str(e)}
        
        finally:
            if self.temp_dir and Path(self.temp_dir).exists():
                try:
                    logger.info("\nCleaning up temporary files...")
                    shutil.rmtree(self.temp_dir)
                    logger.info("✅ Cleanup completed")
                except Exception as e:
                    logger.warning(f"⚠️ Cleanup warning: {str(e)}")
