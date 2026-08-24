"""Main entry point for project generator"""

import logging
import os
import sys
from pathlib import Path

from generator import ProjectGenerator
from utils import setup_logging, load_env_inputs

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    try:
        logger.info("\n" + "="*60)
        logger.info("🚀 ANDROID PROJECT GENERATOR")
        logger.info("="*60 + "\n")
        
        # Load inputs from environment
        logger.info("Loading configuration from environment variables...")
        inputs = load_env_inputs()
        
        logger.info(f"\n📋 Configuration:")
        logger.info(f"   Project Name: {inputs.get('project_name')}")
        logger.info(f"   Package Name: {inputs.get('package_name')}")
        logger.info(f"   Target Repo: {inputs.get('target_repo')}")
        logger.info(f"   Language: {inputs.get('language')}")
        logger.info(f"   Gradle DSL: {inputs.get('gradle_dsl')}")
        logger.info(f"   JDK Version: {inputs.get('jdk_version')}")
        logger.info(f"   Min SDK: {inputs.get('min_sdk')}")
        logger.info(f"   Target SDK: {inputs.get('target_sdk')}\n")
        
        # Generate project
        logger.info("Initializing project generator...\n")
        generator = ProjectGenerator(inputs)
        result = generator.generate_project()
        
        if result['success']:
            logger.info("\n" + "="*60)
            logger.info("✅ SUCCESS - PROJECT CREATED!")
            logger.info("="*60)
            logger.info(f"Project: {result.get('project_name')}")
            logger.info(f"Package: {result.get('package_name')}")
            logger.info(f"Repository: {result.get('repo_url')}")
            logger.info("="*60 + "\n")
            
            # Set GitHub Actions output
            if 'GITHUB_OUTPUT' in os.environ:
                with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
                    f.write(f"repo_url={result.get('repo_url')}\n")
                    f.write(f"project_name={result.get('project_name')}\n")
                    f.write(f"package_name={result.get('package_name')}\n")
            
            sys.exit(0)
        else:
            logger.error("\n" + "="*60)
            logger.error("❌ FAILED - PROJECT GENERATION ERROR")
            logger.error("="*60)
            logger.error(f"Error: {result.get('error')}")
            logger.error("="*60 + "\n")
            sys.exit(1)
    
    except Exception as e:
        logger.error("\n" + "="*60)
        logger.error("❌ FATAL ERROR")
        logger.error("="*60)
        logger.error(f"Exception: {str(e)}", exc_info=True)
        logger.error("="*60 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
