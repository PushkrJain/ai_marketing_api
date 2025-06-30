
# 🧠 Real-Time Multi-Agent AI Marketing Content Generator

## 🔍 Project Summary

Build a **free**, real-time API service that generates **personalized marketing content** (emails, ads, social posts) using **open-source LLMs**. This system is built with a **multi-agent architecture**, includes **robust error logging**, **Prometheus monitoring**, and is fully **containerized** with **Docker**.

---

## 🛠️ Operating System

Recommended:
- **Kali Linux**: Lightweight, secure, and ideal for Docker + open-source workloads.
- **Ubuntu**: More user-friendly alternative, also fully supported.

---

## ⚙️ Technical Stack

| Layer         | Tool/Technology                   | Purpose                                           | Free/Open Source |
|--------------|-----------------------------------|---------------------------------------------------|------------------|
| OS           | Kali Linux / Ubuntu               | Hosting environment                               | ✅               |
| Container    | Docker, Docker Compose            | Reproducible deployment                           | ✅               |
| API Backend  | FastAPI                           | High-performance Python API framework             | ✅               |
| LLM          | Hugging Face Transformers         | Free, open-source LLMs like Phi-3, Mixtral        | ✅               |
| Vector Store | Chroma / FAISS                    | Fast similarity search for segmentation           | ✅               |
| Agents       | Python modules                    | Segmentation, generation, optimization agents     | ✅               |
| Monitoring   | Prometheus, Grafana               | Metrics collection & dashboards                   | ✅               |
| Logging      | Python logging, JSON logs         | Robust error/research logging                     | ✅               |
| Testing      | pytest, HTTPie / curl             | Unit + integration testing                        | ✅               |
| Version Ctrl | Git, GitHub                       | Code management                                   | ✅               |

---

## 🧠 Multi-Agent Architecture

```plaintext
User Profile
    ↓
Segmentation Agent ────┐
                       ↓
            Generation Agent
                       ↓
        ┌─────────────┴─────────────┐
        ↓                           ↓
 User Feedback              Campaign Stats
        ↓                           ↓
 Optimization Agent <──────────────┘
        ↓
 Re-optimized Prompt
        ↓
Re-generation (Optional)
```

### Agent Roles

- **Segmentation Agent**: Clusters customer profiles or retrieves segments from vector store.
- **Generation Agent**: Uses LLM to create marketing copy based on segment and campaign.
- **Optimization Agent**: Adjusts prompts/content using feedback (e.g., engagement scores).

---

## 🧪 Example API Usage

```http
    curl -X POST http://127.0.0.1:8000/generate \
            -H "Content-Type: application/json"\
    -d '{
      "customer_profile": {
    "name": "Alex",
    "segment": "tech_savvy",
    "interests": ["AI", "gadgets"]
  },
  "campaign_type": "email",
  "product": "SmartHome Hub",
  "offer": "Free shipping"
    }'
```

**Response:**
```json
{
  "generated_content": "Hi Alex, as a tech enthusiast, you'll love our SmartHome Hub! Enjoy free shipping this week only..."
}
```

---

## 🧱 Directory Structure

```text
ai-marketing-api/
├── app.py                  # FastAPI app with endpoints and logging
├── agents/
│   ├── segmentation.py     # Segmentation logic
│   ├── generation.py       # LLM content generation
│   └── optimization.py     # Feedback-driven optimization (optional)
├── mylogging/              # error_logger.py, research_logger.py
├── monitoring/             # Prometheus integration
├── db/                     # Feedback persistence logic
├── auth/                   # JWT Authentication logic
├── tests/                  # PyTest test cases
├── hf_models/              # Local HF model storage
├── prometheus.yml          # Prometheus config
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 📊 Monitoring and Logging

### Logging

- Structured logging using Python `logging` module.
- Outputs both console + `.log` files (error.log, research.log).

### Prometheus

- Integrated with `/metrics` using `prometheus-fastapi-instrumentator`.
- Sample config:
```yaml
scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['fastapi-app:8000']
```

### Grafana

- Visualize FastAPI metrics (requests, latency, errors).
- Default: `http://localhost:3000`, login: `admin/admin`.

---

## 🐳 Docker Setup

### Quick Start

```bash
git clone https://github.com/PushkrJain/ai_marketing_api.git
cd ai_marketing_api
sudo docker-compose up --build
```

- Access API: `http://localhost:8000/docs`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

---

## 🔄 Feedback Loop Integration Plan

| Task                         | Description                                      |
|------------------------------|--------------------------------------------------|
| Modify orchestrator.py       | Accept feedback and trigger optimize_prompt     |
| Extend `/create-campaign`    | Accept feedback input                           |
| Add `/regenerate` endpoint   | Optional: re-use feedback to regenerate content |
| Save feedback logs           | Write to .json or SQLite                        |
| Add full feedback tests      | Validate end-to-end loop                        |

---

## ✅ Why Use This Project?

- 100% Open Source, Free to Deploy
- Real-Time Low-Latency APIs (FastAPI + WebSockets)
- Structured Logging + Monitoring (Prometheus + Grafana)
- Modular Multi-Agent System (Extendable, Testable)
- Runs on Any Linux Machine

---

## 📜 License

MIT License. See `LICENSE` for details.

---

## 🙌 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com)
- [Hugging Face](https://huggingface.co)
- [Prometheus](https://prometheus.io)
- [Grafana](https://grafana.com)
- [Docker](https://www.docker.com)

---

## 🤝 Contributing

Pull requests welcome! Please open an issue first to discuss major changes.

---

Enjoy building smarter marketing campaigns with **AI Marketing API**!
