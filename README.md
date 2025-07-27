## About

flightAPI is a challenge‑driven project implementing a high‑performance flight‑search service with FastAPI.  
It exposes endpoints to:

- Search direct flights by origin, destination and date  
- Find valid two‑leg connections  
- Retrieve city, state and country metadata  
- …and more

Please note that I completed this within the estimated timeframe, focusing on the core requirements of the challenge.

## Features

-  **FastAPI** for asynchronous, high‑throughput HTTP handling  
-  **Poetry** for deterministic dependency management  
-  **Dockerized** for easy local and CI/CD deployment  
-  **Alembic** migrations to manage schema changes  
-  **Mock seed data** loader for rapid testing  
-  **Code Style**: PEP8 compliance enforced via Ruff  

## Getting Started

### Prerequisites

- Docker & Docker Compose  
- Python 3.11 (if you want to run scripts locally)  
- (Optional) Make

### Environment Variables

Create a `.env` file in `src/` (ignored by Git) based on `dev.env`:

```bash
cp src/.env.example src/.env
```


### Instructions for setup the application

Run the following commands

```bash
1. make up
2. make migrate
3. make load-data
```



and done! that's all, with that commands you can set up the application and try it.

you can run tests with 
```bash
make test
```


**LOCALLY** check swagger docs in http://127.0.0.1:8000/docs

## Future Improvements

-  Add CI/CD pipelines (linting with Ruff, coverage checks)  
-  Set up dedicated test databases for advanced test scenarios and end-to-end workflows  
-  Integrate Redis caching
-  Containerize with Kubernetes (Pods, Deployments, Helm charts)  
-  Blue/Green or Canary deployments for zero‑downtime releases  




Author: Franco Lema