"""
Git and GitHub operations
"""

import logging
import os
import subprocess
from typing import Dict, Any
from urllib.parse import quote, urlsplit, urlunsplit

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

    def _build_authenticated_url(self, clone_url: str) -> str:
        """Add token auth to HTTPS clone/push URLs."""
        if not self.token:
            return clone_url

        parsed = urlsplit(clone_url)
        if parsed.scheme != 'https' or not parsed.netloc:
            return clone_url

        username = quote(self.actor or 'github-actions', safe='')
        token = quote(self.token, safe='')
        return urlunsplit((
            parsed.scheme,
            f'{username}:{token}@{parsed.netloc}',
            parsed.path,
            parsed.query,
            parsed.fragment,
        ))
    
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
            error_message = str(e)
            if 'Resource not accessible by integration' in error_message:
                error_message = (
                    'GitHub API Error: Repository creation was denied. '
                    'Set GH_TOKEN to a Personal Access Token (PAT) with permission to create repositories; '
                    'the default GitHub Actions GITHUB_TOKEN cannot create a new repository here.'
                )
            else:
                error_message = f"GitHub API Error: {error_message}"
            return {'success': False, 'error': error_message}
    
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
            authenticated_url = self._build_authenticated_url(clone_url)
            subprocess.run(
                ['git', 'clone', authenticated_url, target_path],
                check=True,
                capture_output=True,
                text=True
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
            
            # Push
            remote_url = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()
            subprocess.run(
                ['git', 'remote', 'set-url', 'origin', self._build_authenticated_url(remote_url)],
                check=True,
                capture_output=True
            )
            subprocess.run(['git', 'push', 'origin', branch], check=True, capture_output=True)
            logger.info(f"✅ Changes pushed to origin/{branch}")
            
            os.chdir(original_dir)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to commit/push: {str(e)}")
            os.chdir(original_dir)
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during commit/push: {str(e)}")
            os.chdir(original_dir)
            return False
