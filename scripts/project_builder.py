"""
Project structure builder
"""

import logging
import os
import stat
from pathlib import Path
from utils import format_package_path

logger = logging.getLogger(__name__)

GRADLEW_SCRIPT = """\
#!/usr/bin/env sh
# Gradle wrapper script

APP_NAME="Gradle"
APP_BASE_NAME=`basename "$0"`

# Resolve links: $0 may be a link
PRG="$0"
while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \\(.*\\)$'`
    if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
    else
        PRG=`dirname "$PRG"`"/$link"
    fi
done
SAVED="`pwd`"
cd "`dirname \\"$PRG\\"`/" >/dev/null
APP_HOME="`pwd -P`"
cd "$SAVED" >/dev/null

CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar

# Determine the Java command to use
if [ -n "$JAVA_HOME" ] ; then
    JAVACMD="$JAVA_HOME/bin/java"
else
    JAVACMD="java"
fi

exec "$JAVACMD" -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
"""

GRADLEW_BAT_SCRIPT = """\
@rem Gradle wrapper script for Windows
@if "%DEBUG%" == "" @echo off

set APP_BASE_NAME=%~n0
set APP_HOME=%~dp0

set CLASSPATH=%APP_HOME%gradle\\wrapper\\gradle-wrapper.jar

if defined JAVA_HOME goto init
set JAVACMD=java
goto execute

:init
set JAVACMD=%JAVA_HOME%\\bin\\java.exe

:execute
"%JAVACMD%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
"""

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
            self.base_path / 'app' / 'src' / 'main' / 'res' / 'mipmap-hdpi',
            self.base_path / 'app' / 'src' / 'main' / 'res' / 'mipmap-xhdpi',
            self.base_path / 'app' / 'src' / 'main' / 'res' / 'mipmap-xxhdpi',
            self.base_path / 'app' / 'src' / 'main' / 'res' / 'mipmap-xxxhdpi',
            self.base_path / 'app' / 'src' / 'test' / 'java' / self.package_path,
            self.base_path / 'app' / 'src' / 'androidTest' / 'java' / self.package_path,
            self.base_path / 'gradle' / 'wrapper',
            self.base_path / '.github' / 'workflows',
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created: {dir_path.relative_to(self.base_path)}")
    
    def create_gradle_wrapper(self):
        """Create gradlew and gradlew.bat wrapper scripts"""
        logger.info("Creating Gradle wrapper scripts...")

        gradlew_path = self.base_path / 'gradlew'
        gradlew_path.write_text(GRADLEW_SCRIPT)
        gradlew_path.chmod(gradlew_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        logger.info("Created: gradlew")

        gradlew_bat_path = self.base_path / 'gradlew.bat'
        gradlew_bat_path.write_text(GRADLEW_BAT_SCRIPT)
        logger.info("Created: gradlew.bat")

    def get_package_path(self) -> str:
        """Get package path"""
        return self.package_path
