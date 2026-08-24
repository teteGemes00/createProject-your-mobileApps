#!/usr/bin/env python3
"""
Main entry point untuk project generator
"""

import os
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generator import ProjectGenerator
from utils import setup_logging, load_env_inputs

def main():
    """Main entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Android Project Generator")
        inputs = load_env_inputs()
        logger.info(f"Loaded inputs: {inputs['project_name']}")
        
        generator = ProjectGenerator(inputs)
        logger.info("Generating project...")
        result = generator.generate_project()
        
        if result['success']:
            logger.info("Project created successfully!")
            logger.info(f"Repository: {result['repo_url']}")
            print("\n" + "="*70)
            print("PROJECT CREATED SUCCESSFULLY!")
            print("="*70)
            print(f"Project Name: {inputs['project_name']}")
            print(f"Package: {inputs['package_name']}")
            print(f"Repository: {result['repo_url']}")
            print(f"Language: {inputs['language']}")
            print(f"Gradle DSL: {inputs['gradle_dsl']}")
            print("="*70 + "\n")
            sys.exit(0)
        else:
            logger.error(f"Project generation failed: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
