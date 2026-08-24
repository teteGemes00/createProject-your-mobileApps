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
        logger.info("Starting Android Project Generator...")
        
        # Load inputs from environment
        inputs = load_env_inputs()
        logger.info(f"Inputs loaded: {inputs}")
        
        # Generate project
        generator = ProjectGenerator(inputs)
        result = generator.generate_project()
        
        if result['success']:
            logger.info(f"✅ Project created successfully!")
            logger.info(f"Repository: {result['repo_url']}")
            sys.exit(0)
        else:
            logger.error(f"❌ Project generation failed: {result['error']}")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
