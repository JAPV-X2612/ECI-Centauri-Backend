# 🌌 Exoplanet Detection API

<!-- Logo placeholder -->
<div align="center">
  <img src="assets/images/eci-centauri-logo.jpg" alt="Exoplanet Detection API Logo" width="30%">
</div>

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-0.118.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-App_Service-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-Package_Manager-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)

</div>

---

## 📋 **Table of Contents**

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Development Team](#-development-team)
- [License](#-license)

---

## 🌟 **Overview**

**Exoplanet Detection API** is a backend service developed for the [NASA International Space Apps Challenge](https://www.spaceappschallenge.org/2025/challenges/a-world-away-hunting-for-exoplanets-with-ai/). This *RESTful API* provides **user authentication**, **dataset management**, and **machine learning integration** for detecting potential exoplanets using AI models.

The system allows both **authenticated** and **guest users** to upload astronomical datasets and receive AI-powered predictions, with authenticated users having access to their query history.

---

## ✨ **Features**

### 🔐 **Authentication & Authorization**
- **JWT-based authentication** with secure token generation
- **User registration** with email validation
- **Login system** with bcrypt password hashing
- **Optional authentication** - guest users can use the service without registration

### 👤 **User Management**
- **Complete CRUD operations** for user profiles
- **Self-service account management**
- **Query history tracking** for authenticated users
- **Secure password storage** using bcrypt

### 🤖 **AI Integration** _(Coming Soon)_
- **TensorFlow model integration** for exoplanet detection
- **Dataset upload and processing**
- **Real-time predictions**
- **Result visualization**

### 📊 **API Features**
- **RESTful architecture** with OpenAPI 3.0 specification
- **Comprehensive error handling** with custom exceptions
- **Interactive API documentation** (Swagger UI & ReDoc)
- **CORS support** for frontend integration

---

## 🛠️ **Tech Stack**

### **Backend Framework**
- **FastAPI** `0.118.0` - Modern, high-performance web framework
- **Uvicorn** - ASGI server for production deployment

### **Database**
- **PostgreSQL** `15+` - Relational database (hosted on [Railway](https://railway.app/))
- **SQLAlchemy** `2.0+` - Python SQL toolkit and ORM

### **Security**
- **bcrypt** `4.0+` - Password hashing algorithm
- **python-jose** - JWT token generation and validation
- **Pydantic** - Data validation using Python type hints

### **Machine Learning** _(Integration Pending)_
- **TensorFlow** `2.0+` - Deep learning framework for exoplanet detection

### **Development Tools**
- **Poetry** - Dependency management and packaging
- **pytest** - Testing framework
- **Black** - Code formatter
- **Pylint** - Code linter

---

## 🏗️ **Architecture**

The project follows a **layered architecture** pattern optimized for FastAPI:

```
┌────────────────────────────────────────────┐
│             Frontend (React)               │
│           Static Web App (Azure)           │
└───────────────┬────────────────────────────┘
                │ HTTPS (Axios)
                ↓
┌────────────────────────────────────────────┐
│         FastAPI Backend (Python)           │
│           App Service (Azure)              │
│  ┌──────────────────────────────────────┐  │
│  │    API Layer (Routers/Endpoints)     │  │
│  └────────────┬─────────────────────────┘  │
│               ↓                            │
│  ┌──────────────────────────────────────┐  │
│  │      Business Logic (Services)       │  │
│  └────────────┬─────────────────────────┘  │
│               ↓                            │
│  ┌──────────────────────────────────────┐  │
│  │    Data Access (SQLAlchemy Models)   │  │
│  └──────────────────────────────────────┘  │
└───────────────┬────────────────────────────┘
                │
                ↓
┌────────────────────────────────────────────┐
│       PostgreSQL Database (Railway)        │
└────────────────────────────────────────────┘
```

### **Layer Responsibilities**

| Layer | Components | Purpose |
|-------|-----------|---------|
| **API Layer** | `routers/`, `endpoints/` | Handle HTTP requests, response formatting |
| **Service Layer** | `services/` | Business logic, data validation, orchestration |
| **Data Layer** | `models/` | Database schema, ORM mappings |
| **Schema Layer** | `schemas/` | Request/response validation (Pydantic) |
| **Core** | `core/` | Configuration, security, exceptions |

---

## 📦 **Prerequisites**

Before installation, ensure you have the following installed:

- **Python** `3.11` or higher - [Download](https://www.python.org/downloads/)
- **Poetry** `1.0+` - [Installation Guide](https://python-poetry.org/docs/#installation)
- **PostgreSQL** `15+` - Local installation or [Railway](https://railway.app/) account
- **Git** - [Download](https://git-scm.com/downloads)

---

## 🚀 **Installation**

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/your-org/ECI-Centauri-Backend.git
cd ECI-Centauri-Backend
```

### **2️⃣ Install Poetry** _(if not already installed)_

**Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

**macOS/Linux:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### **3️⃣ Install Dependencies**

```bash
poetry install
```

This command will:
- Create a virtual environment automatically
- Install all production dependencies
- Install development dependencies (pytest, black, pylint)

### **4️⃣ Activate Virtual Environment**

```bash
poetry shell
```

---

## ⚙️ **Configuration**

### **1️⃣ Create Environment File**

Copy the example environment file:

```bash
cp .env.example .env
```

### **2️⃣ Configure Database**

Edit the `.env` file with your PostgreSQL credentials:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name

# Security (Generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=Exoplanet Detection API
```

### **🔑 Generate Secret Key**

**Windows (PowerShell):**
```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

**macOS/Linux:**
```bash
openssl rand -hex 32
```

### **🗄️ Railway PostgreSQL Setup**

1. Create account at [Railway.app](https://railway.app/)
2. Create new project → Add PostgreSQL
3. Copy connection string from Railway dashboard
4. Paste into `DATABASE_URL` in `.env` file

**Example Railway URL format:**
```
postgresql://postgres:password@containers-us-west-123.railway.app:5432/railway
```

---

## ▶️ **Running the Application**

### **Development Mode**

Start the FastAPI development server with auto-reload:

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### **Production Mode**

For production deployment, use Gunicorn with Uvicorn workers:

```bash
poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Parameters:**
- `-w 4` - Number of worker processes (adjust based on CPU cores)
- `-k uvicorn.workers.UvicornWorker` - Use Uvicorn worker class
- `-b 0.0.0.0:8000` - Bind to all interfaces on port 8000

---

## 📖 **API Documentation**

### **Interactive Documentation**

Once the server is running, access the interactive API documentation:

- **Swagger UI** (OpenAPI): http://localhost:8000/docs
  - Test endpoints directly in the browser
  - View request/response schemas
  - See authentication requirements

- **ReDoc** (Alternative UI): http://localhost:8000/redoc
  - Clean, three-panel documentation
  - Better for reading and understanding API structure

### **Available Endpoints**

#### **🔐 Authentication**
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/auth/register` | Register new user | ❌ No |
| `POST` | `/api/v1/auth/login` | Login and get JWT token | ❌ No |

#### **👤 User Management**
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/users/me` | Get current user profile | ✅ Yes |
| `GET` | `/api/v1/users/{id}` | Get user by ID | ✅ Yes |
| `GET` | `/api/v1/users/` | List all users (paginated) | ✅ Yes |
| `PUT` | `/api/v1/users/{id}` | Update user profile | ✅ Yes |
| `DELETE` | `/api/v1/users/{id}` | Delete user account | ✅ Yes |

### **Authentication Flow**

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Database
    
    Client->>API: POST /auth/register
    API->>Database: Create user (hashed password)
    Database-->>API: User created
    API-->>Client: 201 Created + User data
    
    Client->>API: POST /auth/login
    API->>Database: Verify credentials
    Database-->>API: User valid
    API-->>Client: 200 OK + JWT token
    
    Client->>API: GET /users/me (+ JWT)
    API->>API: Validate token
    API->>Database: Get user data
    Database-->>API: User data
    API-->>Client: 200 OK + User profile
```

---

## 🧪 **Testing**

### **Run All Tests**

```bash
poetry run pytest
```

### **Run with Coverage**

```bash
poetry run pytest --cov=app --cov-report=html
```

View coverage report: `htmlcov/index.html`

### **Run Specific Test File**

```bash
poetry run pytest tests/test_auth.py
```

### **Test API Manually with cURL**

**Register User:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=SecurePassword123"
```

**Get Profile (with token):**
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📁 **Project Structure**

```
ECI-Centauri-Backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── auth.py          # Authentication endpoints
│   │       │   └── users.py         # User CRUD endpoints
│   │       ├── __init__.py
│   │       └── dependencies.py      # Auth dependencies
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Environment configuration
│   │   ├── security.py              # Password hashing, JWT
│   │   └── exceptions.py            # Custom exception classes
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py                  # SQLAlchemy User model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py                  # Pydantic schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py          # Business logic
│   │
│   ├── __init__.py
│   ├── database.py                  # Database connection
│   └── main.py                      # FastAPI app entry point
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_users.py
│
├── .env                             # Environment variables (not in git)
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── pyproject.toml                   # Poetry dependencies
├── poetry.lock                      # Locked dependency versions
├── README.md                        # This file
└── LICENSE                          # Project license
```

### **Key Files Explained**

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application initialization, CORS, router registration |
| `app/database.py` | SQLAlchemy engine, session factory, database connection |
| `app/core/config.py` | Load environment variables, centralized configuration |
| `app/core/security.py` | Password hashing (bcrypt), JWT token management |
| `app/core/exceptions.py` | Custom HTTP exceptions with clear error messages |
| `app/models/user.py` | Database schema definition (SQLAlchemy ORM) |
| `app/schemas/user.py` | Request/response validation (Pydantic models) |
| `app/services/user_service.py` | Business logic, database operations, error handling |

---

## 🐛 **Common Issues & Solutions**

### **Issue: Poetry command not found**

**Solution:**
Add Poetry to your PATH:

**Windows:**
```powershell
$Env:Path += ";$Env:APPDATA\Python\Scripts"
```

**macOS/Linux:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### **Issue: bcrypt/passlib compatibility error**

**Solution:**
```bash
poetry remove passlib
poetry add "bcrypt>=4.0.1,<5.0.0"
poetry install
```

### **Issue: Database connection failed**

**Solutions:**
1. Verify `DATABASE_URL` in `.env` file
2. Check Railway database is running
3. Ensure IP is whitelisted in Railway (if applicable)
4. Test connection: `poetry run python -c "from app.database import engine; engine.connect()"`

### **Issue: ImportError - No module named 'email_validator'**

**Solution:**
```bash
poetry add email-validator
poetry install
```

---

## 🚢 **Deployment**

### **Azure App Service**

1. **Create App Service** (Python 3.11, Linux)
2. **Configure environment variables** in Azure Portal
3. **Set startup command:**
   ```bash
   gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app
   ```
4. **Deploy via GitHub Actions** or Azure CLI

**Detailed deployment guide:** [Azure FastAPI Documentation](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)

### **Docker Deployment**

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
```

**Build and run:**
```bash
docker build -t exoplanet-api .
docker run -p 8000:8000 --env-file .env exoplanet-api
```

---

## 👥 **Development Team**

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/JAPV-X2612">
        <img src="https://github.com/JAPV-X2612.png" width="100px;" alt="Jesús Alfonso Pinzón Vega"/>
        <br />
        <sub><b>Jesús Alfonso Pinzón Vega</b></sub>
      </a>
      <br />
      <sub>Backend Developer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/AnderssonProgramming">
        <img src="https://github.com/AnderssonProgramming.png" width="100px;" alt="Andersson David Sánchez Méndez"/>
        <br />
        <sub><b>Andersson David Sánchez Méndez</b></sub>
      </a>
      <br />
      <sub>Backend Developer</sub>
    </td>
  </tr>
</table>

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **NASA Space Apps Challenge** for the inspiration and opportunity
- **FastAPI** community for excellent documentation
- **Railway** for providing database hosting
- **Microsoft Azure** for cloud infrastructure

---

## 📞 **Support**

For questions, issues, or contributions:

- **Issues:** [GitHub Issues](https://github.com/your-org/ECI-Centauri-Backend/issues)
- **Documentation:** http://localhost:8000/docs (when running locally)
- **Email:** team@exoplanet-detection.com

---

<div align="center">
  <p>Made with ❤️ for NASA Space Apps Challenge 2025</p>
  <p>🌟 Star this repository if you find it helpful!</p>
</div>
