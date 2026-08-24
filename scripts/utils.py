"""
Utility functions
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_json_config(config_name: str) -> Dict[str, Any]:
    """Load JSON config file"""
    config_path = Path(__file__).parent.parent / 'config' / f'{config_name}.json'
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    
    with open(config_path, 'r') as f:
        return json.load(f)

def load_env_inputs() -> Dict[str, str]:
    """Load inputs from environment variables"""
    return {
        'project_name': os.getenv('INPUT_PROJECT_NAME', 'MyApp'),
        'package_name': os.getenv('INPUT_PACKAGE_NAME', 'com.example.myapp'),
        'target_repo': os.getenv('INPUT_TARGET_REPO', 'my-app'),
        'app_description': os.getenv('INPUT_APP_DESCRIPTION', 'My Android Application'),
        'language': os.getenv('INPUT_LANGUAGE', 'kotlin'),
        'gradle_dsl': os.getenv('INPUT_GRADLE_DSL', 'kts'),
        'gradle_version': os.getenv('INPUT_GRADLE_VERSION', 'latest'),
        'jdk_version': os.getenv('INPUT_JDK_VERSION', '11'),
        'min_sdk': os.getenv('INPUT_MIN_SDK', '21'),
        'target_sdk': os.getenv('INPUT_TARGET_SDK', '35'),
        'author_name': os.getenv('INPUT_AUTHOR', 'Developer'),
        'company_domain': os.getenv('INPUT_DOMAIN', 'example.com'),
        'github_token': os.getenv('GITHUB_TOKEN', ''),
        'github_actor': os.getenv('GITHUB_ACTOR', 'developer'),
    }

def normalize_jdk_version(version: str) -> str:
    """Convert JDK version to VERSION_X format"""
    return f"VERSION_{version}"

def format_package_path(package_name: str) -> str:
    """Convert package name to path: com.company.app -> com/company/app"""
    return package_name.replace('.', '/')

def create_directories(*paths):
    """Create multiple directories"""
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)

def validate_path(path: str) -> bool:
    """Validate if path is valid"""
    try:
        return Path(path).resolve().is_absolute()
    except:
        return False

def load_template(template_path: str) -> str:
    """Load template file"""
    path = Path(template_path)
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    with open(path, 'r') as f:
        return f.read()

def save_file(file_path: str, content: str):
    """Save content to file"""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        f.write(content)

def get_config_value(config: dict, *keys, default=None):
    """Get nested config value safely"""
    current = config
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return default
    return current if current is not None else default
