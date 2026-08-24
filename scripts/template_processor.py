"""
Template processing and rendering
"""

import logging
from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from utils import save_file

logger = logging.getLogger(__name__)

class TemplateProcessor:
    """Process and render templates"""
    
    def __init__(self, template_dir: str = None):
        if template_dir is None:
            template_dir = str(Path(__file__).parent.parent / 'templates')
        
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            keep_trailing_newline=True
        )
    
    def render_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Render template with variables"""
        try:
            template = self.env.get_template(template_name)
            rendered = template.render(**variables)
            logger.info(f"Rendered: {template_name}")
            return rendered
        except Exception as e:
            logger.error(f"Failed to render {template_name}: {str(e)}")
            raise
    
    def save_rendered_file(self, template_name: str, output_path: str, variables: Dict[str, Any]):
        """Render template and save to file"""
        try:
            content = self.render_template(template_name, variables)
            save_file(output_path, content)
            logger.info(f"Saved: {output_path}")
        except Exception as e:
            logger.error(f"Failed to save {output_path}: {str(e)}")
            raise
