"""
Project structure builder
"""

import logging
from pathlib import Path
from utils import format_package_path

logger = logging.getLogger(__name__)

class ProjectBuilder:
    """Build project directory structure"""
    
    def __init__(self, base_path: str, inputs: dict):
        self.base_path = Path(base_path)
        self.inputs = inputs
        self.package_path = format_package_path(inputs['package_name'])
    
    def create_directory_structure(self):
        """Create all necessary directories"""
        logger.info("Creating directory structure...")
        
        dirs = [
            self.base_path / 'app' / 'src' / 'main' / 'java' / self.package_path,
            self.base_path / 'app' / 'src' / 'main' / 'res' / 'layout',
            self.base_path / 'app' / 'src' / 'main' / 'res' / 'values',
            self.base_path / 'app' / 'src' / 'main' / 'res' / 'drawable',
            self.base_path / 'app' / 'src' / 'main' / 'res' / 'mipmap-mdpi',
            self.base_path / 'app' / 'src' / 'test' / 'java' / self.package_path,
            self.base_path / 'app' / 'src' / 'androidTest' / 'java' / self.package_path,
            self.base_path / 'gradle' / 'wrapper',
            self.base_path / '.github' / 'workflows',
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created: {dir_path.relative_to(self.base_path)}")
    
    def get_package_path(self) -> str:
        """Get package path"""
        return self.package_path
