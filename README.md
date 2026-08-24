# Android Project Generator

Automated Android project generator using templates and GitHub Actions.

## Features

- 🚀 One-click Android project generation
- 🎯 Support for Kotlin and Java
- 📦 Gradle configuration (Groovy & KTS)
- 🔧 Configurable JDK versions
- 📱 SDK level management
- 🔄 Automatic GitHub repository creation
- 📊 CI/CD workflows included

## Quick Start

### Trigger Workflow

1. Go to **Actions** tab
2. Select **Initialize Android Project** workflow
3. Click **Run workflow**
4. Fill in the parameters:
   - Project Name
   - Package Name
   - Target Repository Name
   - Language (Kotlin/Java)
   - SDK Levels
   - JDK Version
5. Add a repository secret named **`GH_TOKEN`** that contains a Personal Access Token (PAT) with permission to create repositories; the default Actions `GITHUB_TOKEN` cannot create the generated repository.

### Supported Languages

- **Kotlin** (Default)
- **Java**

### Gradle DSL

- **KTS** (Kotlin DSL - Default)
- **Groovy** (Traditional)

## Configuration

All configuration is in `config/` directory:

- `android-config.json` - Android SDK and tool versions
- `dependencies.json` - Maven dependencies
- `gradle-versions.json` - Gradle version mappings
- `jdk-versions.json` - JDK version information

## Project Structure

```
createProject-your-mobileApp/
├── .github/workflows/
│   └── init-project.yml              # Main trigger workflow
├── templates/                        # All template files
│   ├── android/                      # Android templates
│   └── workflows/                    # CI/CD workflow templates
├── scripts/                          # Python logic
├── config/                           # Configuration files
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Template System

Templates use Jinja2 for variable substitution:

```jinja2
{{ project_name }}
{{ package_name }}
{{ min_sdk }}
{{ target_sdk }}
```

## Generated Projects

Each generated project includes:

- ✅ Complete Gradle configuration
- ✅ Android resources (layouts, strings, colors)
- ✅ MainActivity template (Kotlin/Java)
- ✅ AndroidManifest.xml
- ✅ ProGuard rules
- ✅ .gitignore
- ✅ CI/CD workflows
- ✅ Documentation (README, SETUP, ARCHITECTURE)

## Requirements

- Python 3.9+
- PyGithub
- Jinja2
- PyYAML

## Development

### Setup

```bash
pip install -r requirements.txt
```

### Testing

```bash
pytest tests/ -v
```

### Linting

```bash
flake8 scripts/
pylint scripts/
black scripts/
```

## License

MIT License - see LICENSE file
