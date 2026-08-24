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
            return {'success': False, 'error': 'GitHub API not available'}
        
        try:
            logger.info(f"Creating repository: {repo_name}")
            
            user = self.github.get_user()
            repo = user.create_repo(
                name=repo_name,
                description=description,
                private=True,
                auto_init=True
            )
            
            logger.info(f"Repository created: {repo.html_url}")
            return {
                'success': True,
                'repo_url': repo.html_url,
                'repo_clone_url': repo.clone_url,
                'repo_name': repo.name
            }
        except Exception as e:
            logger.error(f"Failed to create repository: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def config_git(self, email: str = None, username: str = None):
        """Configure git"""
        if email is None:
            email = f"{self.actor}@users.noreply.github.com"
        if username is None:
            username = self.actor
        
        try:
            subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
            subprocess.run(['git', 'config', '--global', 'user.name', username], check=True)
            logger.info(f"Git configured: {username}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to configure git: {str(e)}")
            raise
    
    def clone_repo(self, clone_url: str, target_path: str) -> bool:
        """Clone repository"""
        try:
            logger.info("Cloning repository...")
            subprocess.run(
                ['git', 'clone', clone_url, target_path],
                check=True,
                capture_output=True
            )
            logger.info(f"Repository cloned")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone: {str(e)}")
            return False
    
    def commit_and_push(self, repo_path: str, message: str, branch: str = 'main') -> bool:
        """Commit and push changes"""
        try:
            os.chdir(repo_path)
            
            subprocess.run(['git', 'add', '-A'], check=True)
            logger.info("Files added")
            
            subprocess.run(['git', 'commit', '-m', message], check=True)
            logger.info("Changes committed")
            
            subprocess.run(['git', 'push', 'origin', branch], check=True)
            logger.info(f"Changes pushed to {branch}")
            
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to commit/push: {str(e)}")
            return False
