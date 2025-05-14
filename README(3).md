
# 🧠 AI Marketing API

## Table of Contents
- [Project Domain](#project-domain)
- [Project Summary & Idea](#project-summary--idea)
- [Technical Stack](#technical-stack)
- [Multi-Agent Architecture](#multi-agent-architecture)
- [Directory Structure](#directory-structure)
- [Setup & Usage](#setup--usage)
  - [System Requirements](#system-requirements)
  - [Local Python Setup](#local-python-setup)
  - [Docker Setup](#docker-setup)
  - [Integrating Hugging Face LLMs](#integrating-hugging-face-llms-optional)
- [API Endpoints](#api-endpoints)
- [Monitoring & Analytics](#monitoring--analytics)
  - [Prometheus](#prometheus)
  - [Grafana](#grafana)
  - [Grafana Dashboard Example](#grafana-dashboard-example)
- [Testing](#testing)
- [Production & Security Notes](#production--security-notes)
- [Maintenance & Docker Tips](#maintenance--docker-tips)
- [Feedback Loop Integration Plan](#feedback-loop-integration-plan)
- [Why Use This Project?](#why-use-this-project)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Project Domain

**AI-powered Marketing Automation & Analytics**  
Automate, personalize, and optimize marketing content generation, segmentation, and feedback analytics using open-source LLMs and a robust multi-agent architecture.

---

## Project Summary & Idea

**AI Marketing API** is a real-time, containerized API service for generating personalized marketing content (emails, ads, social posts) using open-source LLMs.  
- Multi-agent architecture for segmentation, content generation, and optimization.
- Robust error logging, Prometheus monitoring, and Grafana dashboards.
- Fully open-source and free to deploy on any Linux machine.

---

## Technical Stack

| Layer         | Tool/Technology           | Purpose                                | Open Source |
|---------------|--------------------------|----------------------------------------|-------------|
| OS            | Kali Linux / Ubuntu      | Hosting environment                    | ✅          |
| Container     | Docker, Docker Compose   | Reproducible deployment                | ✅          |
| API Backend   | FastAPI                  | High-performance Python API framework  | ✅          |
| LLM           | Hugging Face Transformers| Open-source LLMs (Phi-3, Mixtral, etc.)| ✅         |
| Vector Store  | Chroma / FAISS           | Segmentation & similarity search       | ✅          |
| Agents        | Python modules           | Segmentation, generation, optimization | ✅          |
| Monitoring    | Prometheus, Grafana      | Metrics & dashboards                   | ✅          |
| Logging       | Python logging           | Structured error/research logging      | ✅          |
| Testing       | pytest, HTTPie/curl      | Unit & integration testing             | ✅          |
| Version Ctrl  | Git, GitHub              | Code management                        | ✅          |

---

## Multi-Agent Architecture

User Profile  
↓  
Segmentation Agent ────┐  
↓  
Generation Agent  
↓  
┌─────────────┴─────────────┐  
↓ ↓  
User Feedback Campaign Stats  
↓ ↓  
Optimization Agent <──────────────┘  
↓  
Re-optimized Prompt  
↓  
Re-generation (Optional)  

**Agent Roles:**  
- **Segmentation Agent:** Clusters customer profiles or retrieves segments from vector store.  
- **Generation Agent:** Uses LLM to create marketing copy based on segment and campaign.  
- **Optimization Agent:** Adjusts prompts/content using feedback (e.g., engagement scores).  

---

## Directory Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
├── agent/
│   ├── __init__.py
│   ├── generation.py
│   ├── optimization.py
│   ├── orchestrator.py
│   └── segmentation.py
├── auth/
│   └── auth.py
├── db/
│   ├── __init__.py
│   └── feedback.py
├── monitoring/
│   ├── __init__.py
│   └── metrics.py
├── mylogging/
│   ├── __init__.py
│   ├── error_logger.py
│   └── research_logger.py
├── hf_models/
│   └── phi3/
├── logs/
│   ├── error.log
│   └── research.log
├── prometheus.yml
├── prometheus-2.53.0.linux-amd64/
│   ├── prometheus
│   ├── prometheus.yml
│   └── ...
├── tests/
│   ├── test_api.py
│   └── test_full_api.py
└── feedback.db
```

---

## Setup & Usage

### System Requirements

- Linux (Kali or Ubuntu recommended)  
- Docker & Docker Compose  
- (Optional) Python 3.10+ and venv for local runs  

### Local Python Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

### Docker Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
git clone https://github.com/PushkrJain/ai_marketing_api.git
cd ai_marketing_api
sudo docker-compose up --build
```

- API: [http://localhost:8000/docs](http://localhost:8000/docs)  
- Prometheus: [http://localhost:9090](http://localhost:9090)  
- Grafana: [http://localhost:3000](http://localhost:3000)  

### Integrating Hugging Face LLMs (Optional)

```bash
sudo apt install git-lfs
git lfs install
mkdir -p ~/hf_models/phi3
cd ~/hf_models/phi3
git clone https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
mv ~/hf_models ~/ai-marketing-api/
```

---

## API Endpoints

| Endpoint            | Method | Description                          |
|---------------------|--------|--------------------------------------|
| `/generate-content` | POST   | Generate personalized marketing copy |
| `/create-campaign`  | POST   | Create a new campaign                |
| `/feedback`         | POST   | Submit feedback                      |
| `/metrics`          | GET    | Prometheus metrics                   |
| `/docs`             | GET    | Swagger documentation UI             |

**Example Request:**

```bash
curl -X POST http://127.0.0.1:8000/generate-content -H "Content-Type: application/json" -d '{"customer_profile": {"name": "Alex", "segment": "tech_savvy", "interests": ["AI", "gadgets"]}, "campaign_type": "email", "product": "SmartHome Hub", "offer": "Free shipping"}'
```

**Example Response:**
```json
{
  "generated_content": "Hi Alex, as a tech enthusiast, you'll love our SmartHome Hub! Enjoy free shipping this week only..."
}
```

---

## Monitoring & Analytics

### Logging

- Structured logs: `logs/error.log`, `logs/research.log`  
- Console + file output for traceability  

### Prometheus

- Metrics scraped from `/metrics`  
- Sample config:

```yaml
scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['fastapi-app:8000']
```

### Grafana

- Visualizes Prometheus metrics  
- Default login: `admin` / `admin`  

---

## Grafana Dashboard Example

> Screenshot (e.g., `docs/grafana_dashboard.png`) recommended here.

---

## Testing

```bash
pytest
```

**Example using `curl`:**

See example under [API Endpoints](#api-endpoints).

---

## Production & Security Notes

- **Use PostgreSQL** in production  
- **Never commit secrets**; use `.env`  
- **Secure Docker** exposure  
- **Monitoring** critical via Prometheus & Grafana  

---

## Maintenance & Docker Tips

```bash
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi -f $(sudo docker images -aq)
sudo docker system prune -af --volumes
tail -f logs/error.log logs/research.log
```

---

## Feedback Loop Integration Plan

| Task                    | Description                                 |
|-------------------------|---------------------------------------------|
| Update `orchestrator.py`| Accept and pass feedback                    |
| Extend API              | Accept feedback JSON and logs               |
| Regenerate Endpoint     | (Optional) Feedback-driven regeneration     |
| Store Feedback          | In SQLite `.db` or JSON log                 |
| End-to-End Tests        | Validate full feedback cycle                |

---

## Why Use This Project?

- Open Source & Free  
- Real-Time API using FastAPI  
- Modular Agents, Fully Testable  
- Monitoring (Prometheus + Grafana)  
- Deployable Anywhere (Linux + Docker)  

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)  
- [Hugging Face](https://huggingface.co/)  
- [Prometheus](https://prometheus.io/)  
- [Grafana](https://grafana.com/)  
- [Docker](https://www.docker.com/)  

---

## Contributing

Pull requests welcome. Open issues to propose changes.

---

## Contact

**Pushkar Jain** — AI Marketing API Maintainer  
GitHub: [PushkrJain](https://github.com/PushkrJain)  
Email: *available on GitHub profile*

---

*Enjoy building smarter marketing campaigns with AI Marketing API!*
