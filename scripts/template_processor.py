"""
Template processing and rendering with Jinja2
"""

import logging
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, select_autoescape, StrictUndefined
from utils import save_file, format_package_path

logger = logging.getLogger(__name__)

class TemplateProcessor:
    """Process and render Jinja2 templates"""
    
    def __init__(self, template_dir: str = None):
        if template_dir is None:
            template_dir = str(Path(__file__).parent.parent / 'templates')
        
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Render template with variables"""
        try:
            template = self.env.get_template(template_name)
            rendered = template.render(**variables)
            logger.info(f"✅ Rendered: {template_name}")
            return rendered
        except Exception as e:
            logger.error(f"❌ Failed to render {template_name}: {str(e)}")
            raise
    
    def save_rendered_file(self, template_name: str, output_path: str, variables: Dict[str, Any]):
        """Render template and save to file"""
        try:
            content = self.render_template(template_name, variables)
            save_file(output_path, content)
            logger.info(f"✅ Saved: {output_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save {output_path}: {str(e)}")
            raise
    
    def process_project_templates(self, output_base_path: str, variables: Dict[str, Any], gradle_dsl: str = 'kts'):
        """Process all project templates and save to output directory"""
        try:
            logger.info(f"\n📋 Processing project templates (Gradle DSL: {gradle_dsl})...")
            
            # Gradle file extension based on DSL
            gradle_ext = '.kts' if gradle_dsl == 'kts' else ''
            
            # Map of template files to output paths
            template_mappings = [
                # Gradle files
                (f'android/gradle/build.gradle{gradle_ext}.template', 
                 f'{output_base_path}/build.gradle{gradle_ext}'),
                (f'android/gradle/settings.gradle{gradle_ext}.template', 
                 f'{output_base_path}/settings.gradle{gradle_ext}'),
                (f'android/gradle/gradle.properties.template', 
                 f'{output_base_path}/gradle.properties'),
                
                # App module gradle
                (f'android/app/build.gradle{gradle_ext}.template', 
                 f'{output_base_path}/app/build.gradle{gradle_ext}'),
                (f'android/app/proguard-rules.pro.template', 
                 f'{output_base_path}/app/proguard-rules.pro'),
                (f'android/app/proguard-advanced.pro.template', 
                 f'{output_base_path}/app/proguard-advanced.pro'),
                
                # AndroidManifest
                ('android/app/src/main/AndroidManifest.xml.template', 
                 f'{output_base_path}/app/src/main/AndroidManifest.xml'),
                
                # Layout files
                ('android/app/src/main/res/layout/activity_main.xml.template', 
                 f'{output_base_path}/app/src/main/res/layout/activity_main.xml'),
                
                # Resource files
                ('android/app/src/main/res/values/strings.xml.template', 
                 f'{output_base_path}/app/src/main/res/values/strings.xml'),
                ('android/app/src/main/res/values/colors.xml.template', 
                 f'{output_base_path}/app/src/main/res/values/colors.xml'),
                ('android/app/src/main/res/values/styles.xml.template', 
                 f'{output_base_path}/app/src/main/res/values/styles.xml'),
                ('android/app/src/main/res/values/dimens.xml.template', 
                 f'{output_base_path}/app/src/main/res/values/dimens.xml'),
                
                # Root config files
                ('android/root/.gitignore.template', 
                 f'{output_base_path}/.gitignore'),
                ('android/root/gradle-wrapper.properties.template', 
                 f'{output_base_path}/gradle/wrapper/gradle-wrapper.properties'),
                ('android/root/local.properties.template', 
                 f'{output_base_path}/local.properties'),
                
                # Launcher icons
                ('android/app/src/main/res/mipmap/ic_launcher.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-mdpi/ic_launcher.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-hdpi/ic_launcher.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-xhdpi/ic_launcher.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-xxhdpi/ic_launcher.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-xxxhdpi/ic_launcher.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher_round.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-mdpi/ic_launcher_round.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher_round.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-hdpi/ic_launcher_round.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher_round.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-xhdpi/ic_launcher_round.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher_round.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.xml'),
                ('android/app/src/main/res/mipmap/ic_launcher_round.xml.template',
                 f'{output_base_path}/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.xml'),
                
                # Documentation
                ('android/docs/README.md.template', 
                 f'{output_base_path}/README.md'),
                ('android/docs/SETUP.md.template', 
                 f'{output_base_path}/docs/SETUP.md'),
                ('android/docs/CONTRIBUTING.md.template', 
                 f'{output_base_path}/docs/CONTRIBUTING.md'),
                ('android/docs/ARCHITECTURE.md.template', 
                 f'{output_base_path}/docs/ARCHITECTURE.md'),
                ('android/docs/CHANGELOG.md.template', 
                 f'{output_base_path}/docs/CHANGELOG.md'),
            ]
            
            # Determine language extension
            language_ext = '.kt' if variables.get('language') == 'kotlin' else '.java'
            package_path = format_package_path(variables.get('package_name', 'com.example.myapp'))
            
            # Add MainActivity based on language
            if language_ext == '.kt':
                template_mappings.append((
                    'android/app/src/main/java/PACKAGE_PATH/MainActivity.kt.template',
                    f'{output_base_path}/app/src/main/java/{package_path}/MainActivity.kt'
                ))
            else:
                template_mappings.append((
                    'android/app/src/main/java/PACKAGE_PATH/MainActivity.java.template',
                    f'{output_base_path}/app/src/main/java/{package_path}/MainActivity.java'
                ))
            
            # Process all templates
            for template_path, output_path in template_mappings:
                try:
                    self.save_rendered_file(template_path, output_path, variables)
                except Exception as e:
                    logger.warning(f"⚠️ Skipping {template_path}: {str(e)}")
            
            logger.info(f"\n✅ All templates processed successfully!")
            return True
        
        except Exception as e:
            logger.error(f"❌ Template processing failed: {str(e)}")
            raise
    
    def process_workflow_templates(self, output_path: str, variables: Dict[str, Any]):
        """Process workflow templates"""
        try:
            logger.info(f"\n📋 Processing workflow templates...")
            
            workflow_mappings = [
                ('workflows/build.yml.template', f'{output_path}/build.yml'),
                ('workflows/setup-keystore.yml.template', f'{output_path}/setup-keystore.yml'),
            ]
            
            for template_path, output_file_path in workflow_mappings:
                self.save_rendered_file(template_path, output_file_path, variables)
            
            logger.info(f"✅ Workflow templates processed!")
            return True
        
        except Exception as e:
            logger.error(f"❌ Workflow processing failed: {str(e)}")
            raise
