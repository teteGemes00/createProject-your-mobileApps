"""
Generate workflow files
"""

import logging
from pathlib import Path
from template_processor import TemplateProcessor

logger = logging.getLogger(__name__)

class WorkflowGenerator:
    """Generate GitHub Actions workflows"""

    def __init__(self, template_dir=None):
        self.processor = TemplateProcessor(template_dir)

    def generate_all(self, output_path: str, variables: dict):
        """Generate all workflow templates"""
        workflows = [
            ('workflows/build.yml.template', 'build.yml'),
            ('workflows/setup-keystore.yml.template', 'setup-keystore.yml'),
        ]
        Path(output_path).mkdir(parents=True, exist_ok=True)
        for tpl, out in workflows:
            try:
                self.processor.save_rendered_file(tpl, str(Path(output_path) / out), variables)
                logger.info(f"✅ Workflow generated: {out}")
            except Exception as e:
                logger.warning(f"⚠️ Skipping {tpl}: {str(e)}")
        return True

    def generate_build_yml(self, inputs: dict, output_path: str, variables: dict):
        """Generate build.yml workflow"""
        logger.info("Generating build.yml")
        return self.processor.save_rendered_file(
            'workflows/build.yml.template',
            str(Path(output_path) / 'build.yml'),
            variables
        )

    def generate_keystore_yml(self, inputs: dict, output_path: str, variables: dict):
        """Generate setup-keystore.yml workflow"""
        logger.info("Generating setup-keystore.yml")
        return self.processor.save_rendered_file(
            'workflows/setup-keystore.yml.template',
            str(Path(output_path) / 'setup-keystore.yml'),
            variables
        )
