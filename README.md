# createProject-your-mobileApps

🚀 **Automated Android Project Generator** - Membuat Android project baru dengan mudah, seperti IDE!

## 📋 Overview

Repo ini adalah automation tool yang membuat Android project baru dengan struktur lengkap, modular, dan siap production - **seperti Android Studio**.

**Workflow:** 
1. Trigger `init-project.yml` 
2. Isi form input lengkap
3. Workflow otomatis generate project + repo baru
4. Done! Project siap development

## 🎯 Features

- ✅ IDE-like input form (Project Name, Package, Language, SDK, JDK, dll)
- ✅ Auto repository creation di GitHub
- ✅ Full project structure generation
- ✅ Multi-language support (Kotlin/Java)
- ✅ Multi Gradle support (KTS/Groovy)
- ✅ All SDK levels supported (9-36)
- ✅ Included workflows (build.yml, setup-keystore.yml)
- ✅ Complete documentation
- ✅ Production-ready ProGuard rules

## 🚀 Quick Start

1. Go ke: **Actions** → **Initialize Android Project**
2. Click **Run workflow**
3. Fill form dengan detail project Anda
4. Wait for completion
5. New repository created! 🎉

## 📁 Struktur Repo

```
createProject-your-mobileApps/
├── .github/workflows/
│   └── init-project.yml
├── templates/
│   ├── android/
│   └── workflows/
├── scripts/
├── config/
├── requirements.txt
└── README.md
```

## 🔧 How It Works

1. **Input Form** - User mengisi form dengan detail project
2. **Validation** - Python script validate semua input
3. **Generation** - Template dirender dengan variable
4. **GitHub Repo** - Repo baru dibuat otomatis
5. **Commit** - Semua files di-commit dan di-push
6. **Workflows** - build.yml dan setup-keystore.yml di-generate
7. **Done** - Project siap development

## 📝 Input Form Options

| Input | Type | Options | Default |
|-------|------|---------|----------|
| Project Name | Text | Any | MyApp |
| Package Name | Text | com.company.app | com.example.myapp |
| Target Repo | Text | Any | - |
| Language | Choice | kotlin, java | kotlin |
| Gradle DSL | Choice | kts, groovy | kts |
| Gradle Version | Choice | latest, 8.4, 8.3, ... | latest |
| JDK | Choice | 8-21 | 11 |
| Min SDK | Choice | 9-36 | 21 |
| Target SDK | Choice | 28-36 | 35 |
| Author | Text | Any | Developer |
| Domain | Text | Any | example.com |

## 📦 Requirements

```
Jinja2==3.1.2
PyGithub==2.1.1
python-dotenv==1.0.0
requests==2.31.0
pyyaml==6.0.1
```

## 📚 Documentation

- Configuration: See `config/` folder
- Templates: See `templates/` folder
- Scripts: See `scripts/` folder

## 🔐 Security

- Uses GitHub token for repository creation
- Repositories created as **private** by default
- Token scoped to: `contents:write`, `repo`

## 🤝 Contributing

Pull requests welcome!

## 📄 License

MIT License

---

**Made with ❤️ for Android Developers**
