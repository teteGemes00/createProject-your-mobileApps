"""
Input validation
"""

import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class InputValidator:
    """Validate all user inputs"""
    
    def __init__(self, config: dict):
        self.config = config
    
    def validate_all(self, inputs: dict) -> Tuple[bool, str]:
        """Validate all inputs"""
        
        validators = [
            (self.validate_project_name, inputs.get('project_name')),
            (self.validate_package_name, inputs.get('package_name')),
            (self.validate_repo_name, inputs.get('target_repo')),
            (self.validate_jdk_version, inputs.get('jdk_version')),
            (self.validate_gradle_version, inputs.get('gradle_version')),
            (self.validate_sdk_levels, (inputs.get('min_sdk'), inputs.get('target_sdk'))),
        ]
        
        for validator, value in validators:
            is_valid, message = validator(value)
            if not is_valid:
                logger.error(f"Validation failed: {message}")
                return False, message
            logger.info(f"Valid: {message}")
        
        return True, "All inputs valid"
    
    def validate_project_name(self, name: str) -> Tuple[bool, str]:
        """Validate project name"""
        if not name or len(name) < 2 or len(name) > 50:
            return False, "Project name must be 2-50 characters"
        
        pattern = self.config.get('projectNamePattern', '^[a-zA-Z0-9\\s-]+$')
        if not re.match(pattern, name):
            return False, "Project name contains invalid characters"
        
        return True, f"Project name '{name}'"
    
    def validate_package_name(self, package: str) -> Tuple[bool, str]:
        """Validate package name"""
        if not package:
            return False, "Package name is required"
        
        pattern = self.config.get('packagePattern', '^[a-z][a-z0-9]*(\\.[a-z0-9]+)*$')
        if not re.match(pattern, package):
            return False, "Invalid package name format"
        
        return True, f"Package name '{package}'"
    
    def validate_repo_name(self, repo: str) -> Tuple[bool, str]:
        """Validate GitHub repo name"""
        if not repo or len(repo) < 1 or len(repo) > 39:
            return False, "Repo name must be 1-39 characters"
        
        pattern = self.config.get('repoNamePattern', '^[a-z0-9]([a-z0-9-]*[a-z0-9])?$')
        if not re.match(pattern, repo):
            return False, "Repo name contains invalid characters"
        
        return True, f"Repo name '{repo}'"
    
    def validate_jdk_version(self, version: str) -> Tuple[bool, str]:
        """Validate JDK version"""
        valid_versions = self.config.get('jdk', {}).get('versions', [])
        
        if version not in valid_versions:
            return False, f"Invalid JDK version"
        
        return True, f"JDK version {version}"
    
    def validate_gradle_version(self, version: str) -> Tuple[bool, str]:
        """Validate Gradle version"""
        valid_versions = self.config.get('gradle', {}).get('versions', {})
        
        if version not in valid_versions:
            return False, f"Invalid Gradle version"
        
        return True, f"Gradle version {version}"
    
    def validate_sdk_levels(self, levels: Tuple[str, str]) -> Tuple[bool, str]:
        """Validate SDK levels"""
        min_sdk, target_sdk = levels
        
        try:
            min_val = int(min_sdk)
            target_val = int(target_sdk)
        except (ValueError, TypeError):
            return False, "SDK levels must be numeric"
        
        if min_val > target_val:
            return False, "Min SDK cannot be greater than Target SDK"
        
        return True, f"SDK {min_sdk}-{target_sdk}"
