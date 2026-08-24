"""
Git and GitHub operations
"""

import logging
import os
import subprocess
from typing import Dict, Any

try:
    from github import Github
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

logger = logging.getLogger(__name__)

class GitHelper:
    """Handle Git and GitHub operations"""
    
    def __init__(self, token: str, actor: str):
        self.token = token
        self.actor = actor
        if GITHUB_AVAILABLE and token:
            self.github = Github(token)
        else:
            self.github = None
    
    def create_github_repo(self, repo_name: str, description: str) -> Dict[str, Any]:
        """Create GitHub repository"""
        if not self.github:
            logger.warning("GitHub API not available")
            return {'success': False, 'error': 'GitHub API not available. Please ensure PyGithub is installed.'}
        
        try:
            logger.info(f"Creating repository: {repo_name}")
            
            user = self.github.get_user()
            repo = user.create_repo(
                name=repo_name,
                description=description,
                private=False,
                auto_init=True
            )
            
            logger.info(f"✅ Repository created: {repo.html_url}")
            return {
                'success': True,
                'repo_url': repo.html_url,
                'repo_clone_url': repo.clone_url,
                'repo_name': repo.name
            }
        except Exception as e:
            logger.error(f"❌ Failed to create repository: {str(e)}")
            return {'success': False, 'error': f"GitHub API Error: {str(e)}"}
    
    def config_git(self, email: str = None, username: str = None):
        """Configure git"""
        if email is None:
            email = f"{self.actor}@users.noreply.github.com"
        if username is None:
            username = self.actor
        
        try:
            subprocess.run(['git', 'config', '--global', 'user.email', email], check=True, capture_output=True)
            subprocess.run(['git', 'config', '--global', 'user.name', username], check=True, capture_output=True)
            logger.info(f"✅ Git configured: {username} <{email}>")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to configure git: {str(e)}")
            raise
    
    def clone_repo(self, clone_url: str, target_path: str) -> bool:
        """Clone repository"""
        try:
            logger.info(f"Cloning repository from: {clone_url}")
            
            # Use token in clone URL for authentication
            if self.token and 'https://' in clone_url:
                clone_url = clone_url.replace('https://', f'https://{self.actor}:{self.token}@')
            
            result = subprocess.run(
                ['git', 'clone', clone_url, target_path],
                check=True,
                capture_output=True,
                text=True,
                env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'}
            )
            logger.info(f"✅ Repository cloned to: {target_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to clone: {e.stderr}")
            return False
    
    def commit_and_push(self, repo_path: str, message: str, branch: str = 'main') -> bool:
        """Commit and push changes"""
        try:
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            # Check if there are changes
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                check=True
            )
            
            if not status_result.stdout.strip():
                logger.info("⚠️ No changes to commit")
                os.chdir(original_dir)
                return True
            
            # Add all files
            subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
            logger.info("✅ Files added")
            
            # Commit
            subprocess.run(['git', 'commit', '-m', message], check=True, capture_output=True)
            logger.info(f"✅ Changes committed with message: '{message}'")
            
            # Check current branch
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            current_branch = branch_result.stdout.strip()
            logger.info(f"Current branch: {current_branch}")
            
            # If we're on a detached HEAD, checkout the target branch first
            if current_branch == 'HEAD':
                logger.info(f"Checking out branch: {branch}")
                subprocess.run(['git', 'checkout', '-b', branch], check=True, capture_output=True)
            
            # Push with token authentication
            env = os.environ.copy()
            if self.token:
                env['GIT_ASKPASS'] = ''
                env['GIT_TERMINAL_PROMPT'] = '0'
            
            subprocess.run(
                ['git', 'push', 'origin', branch],
                check=True,
                capture_output=True,
                env=env
            )
            logger.info(f"✅ Changes pushed to origin/{branch}")
            
            os.chdir(original_dir)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to commit/push: {str(e)}")
            logger.error(f"Error details: {e.stderr if e.stderr else 'No stderr'}")
            os.chdir(original_dir)
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during commit/push: {str(e)}")
            os.chdir(original_dir)
            return False
