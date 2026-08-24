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

def build_template_variables(inputs: dict, config: dict) -> Dict[str, Any]:
    """Build template variables from inputs and config"""
    jdk_ver = inputs.get('jdk_version', '11')
    gradle_ver = inputs.get('gradle_version', 'latest')
    
    # Get dependency versions from config
    dependencies = config.get('dependencies', {})
    androidx = dependencies.get('androidx', {})
    testing = dependencies.get('testing', {})
    androidx_test = dependencies.get('androidx-test', {})
    
    # Get gradle versions
    gradle_config = config.get('gradle', {})
    gradle_versions = gradle_config.get('versions', {})
    resolved_gradle_version = gradle_versions.get(gradle_ver, gradle_versions.get('latest', '8.5.0'))
    
    # Get kotlin version from config
    kotlin_config = config.get('kotlin', {})
    kotlin_version = kotlin_config.get('version', '1.9.20')
    
    # Build variable dict
    template_vars = {
        # Project info
        'project_name': inputs.get('project_name', 'MyApp'),
        'project_name_clean': inputs.get('project_name', 'MyApp').replace(' ', '').replace('-', ''),
        'package_name': inputs.get('package_name', 'com.example.myapp'),
        'app_description': inputs.get('app_description', 'My Android Application'),
        'description': inputs.get('app_description', 'My Android Application'),
        
        # Build configuration
        'language': inputs.get('language', 'kotlin'),
        'language_ext': 'kt' if inputs.get('language') == 'kotlin' else 'java',
        'gradle_dsl': inputs.get('gradle_dsl', 'kts'),
        'gradle_version': resolved_gradle_version,
        'jdk_version': jdk_ver,
        'kotlin_version': kotlin_version,
        
        # SDK levels
        'min_sdk': inputs.get('min_sdk', '21'),
        'target_sdk': inputs.get('target_sdk', '35'),
        'compile_sdk': config.get('compileSdk', 35),
        
        # Build info
        'version_code': config.get('version_code', 1),
        'version_name': config.get('version_name', '1.0.0'),
        'build_tools_version': config.get('build_tools_version', '35.0.0'),
        'android_gradle_plugin': config.get('android_gradle_plugin', '8.2.0'),
        
        # Author info
        'author': inputs.get('author_name', 'Developer'),
        'domain': inputs.get('company_domain', 'example.com'),
        
        # GitHub info
        'github': inputs.get('github_actor', 'developer'),
        'github_actor': inputs.get('github_actor', 'developer'),
        
        # Dependencies
        'androidx_appcompat': androidx.get('appcompat', '1.6.1'),
        'androidx_constraint_layout': androidx.get('constraintLayout', '2.1.4'),
        'androidx_material': androidx.get('material', '1.11.0'),
        'androidx_lifecycle': androidx.get('lifecycle-runtime', '2.7.0'),
        'androidx_activity': androidx.get('activity', '1.8.0'),
        'androidx_fragment': androidx.get('fragment', '1.6.2'),
        'material': config.get('dependencies', {}).get('google', {}).get('material', '1.11.0'),
        'junit': testing.get('junit', '4.13.2'),
        'androidx_test_ext_junit': androidx_test.get('ext-junit', '1.1.5'),
        'androidx_test_espresso_core': androidx_test.get('espresso-core', '3.5.1'),
    }
    
    return template_vars

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
