# Synonym Service (FastAPI)

This project implements a **Synonym Service API** using **FastAPI**, **Azure SQL Edge**, and **Redis**.  
It provides efficient synonym lookups with caching, structured logging, retry mechanisms, and graceful shutdown handling — designed to demonstrate production-grade backend design principles.

---

## 🚀 Overview

The Synonym Service:
- Serves synonym lookup requests over REST API endpoints.
- Uses **SQL Server** as the primary data store.
- Implements **Redis caching** (or in-memory fallback) to reduce latency.
- Includes structured logging, error handling, and health monitoring endpoints.

**Tech Stack:**
- Python 3.11  
- FastAPI (Web framework)  
- Redis (Cache)  
- Azure SQL Edge (Database)  
- Docker Compose (Container orchestration)

---

## 🧱 Project Structure

synonym_service/
├── app/
│ ├── api/ # FastAPI routes and controllers
│ ├── cache/ # Redis / memory cache logic
│ ├── core/ # Logging, configuration, startup events
│ ├── db/ # SQL Server repository layer
│ └── services/ # Business logic for synonyms
├── tests/ # Test cases (cache, API, memory strategy)
├── Dockerfile # FastAPI app container
├── docker-compose.yml # Runs API + SQL Edge + Redis
├── requirements.txt # Python dependencies
├── seed.sql # Database initialization script
├── .env # Environment configuration
└── README.md



---

## 🧩 Features

✅ FastAPI app with clean modular structure  
✅ SQL Server + Redis integration  
✅ Configurable TTL caching (via `.env`)  
✅ Health check endpoint `/healthz`  
✅ Dockerized and production-ready  

---

## ⚙️ Running the Project

### 1️⃣ Prerequisites
- Install **Docker Desktop**
- (macOS) Install SQL tools:
  ```bash
  brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
  brew update
  ACCEPT_EULA=Y brew install --no-quarantine msodbcsql18 mssql-tools18

2️⃣ Build & Start Services
cd ~/Downloads/synonym_service
docker compose up -d --build


This launches:

sqledge → SQL Server (port 1433)

redis → Redis cache (port 6379)

synonym-service → FastAPI app (port 8000)

3️⃣ Seed the Database
/opt/homebrew/opt/mssql-tools18/bin/sqlcmd \
  -S 127.0.0.1,1433 -U sa -P 'YourStrong!Passw0rd' -C -i seed.sql

4️⃣ Test Health Endpoint
curl http://localhost:8000/healthz


Expected:

{"status": "ok"}


You can also explore the API:

Swagger UI → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

5️⃣ Stop Containers
docker compose down -v

🌱 Environment Variables

Configured in .env:

APP_NAME=synonym-service
CACHE_BACKEND=memory
CACHE_TTL_SECONDS=600

SQLSERVER_HOST=sqledge
SQLSERVER_PORT=1433
SQLSERVER_USER=sa
SQLSERVER_PASSWORD=YourStrong!Passw0rd
SQLSERVER_DB=SynonymsDB

REDIS_URL=redis://redis:6379

🧪 Tests

Run unit tests (optional):

pytest -v
