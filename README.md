# Stock Market Data Platform 📈

A production-style **Data Engineering platform** that ingests, processes, 
and serves real-time stock market data using industry-standard tools.

## Architecture

![Architecture](images/architecture.png)

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Ingestion | Apache Kafka | Real-time message streaming |
| Stream Processing | Apache Flink | Real-time aggregations |
| Batch Processing | Apache Spark | Nightly lakehouse ETL |
| Lakehouse | Delta Lake | Bronze/Silver/Gold layers |
| Object Storage | MinIO | S3-compatible file storage |
| Database | PostgreSQL | Structured data storage |
| API | FastAPI | REST API serving |
| Containerization | Docker + Compose | Full stack deployment |

## Services

| Service | Port | Description |
|---|---|---|
| FastAPI | 8000 | REST API + Swagger docs |
| Flink Dashboard | 8081 | Job monitoring UI |
| MinIO Console | 9001 | Object storage UI |
| Kafka | 9092 | Message broker |
| PostgreSQL | 5433 | Database |

## Quick Start

**Prerequisites:** Docker Desktop installed and running
```bash
# Clone the repo
git clone https://github.com/phanbahoangkhanh/stock-market-data-platform.git
cd stock-market-data-platform

# Start entire stack with one command
docker compose up -d
```

That's it. All services start automatically.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/prices` | Latest price for all 5 stocks |
| GET | `/prices/{symbol}` | Full price history for one stock |
| GET | `/stats` | Platform statistics |
| GET | `/alerts` | Price drop alerts |
| GET | `/docs` | Interactive Swagger documentation |

### Example Response
```bash
curl http://localhost:8000/prices
```
```json
{
  "data": [
    {"symbol": "AAPL", "price": 252.52, "volume": 46144088, "fetched_at": "2026-03-23T14:49:30"},
    {"symbol": "GOOGL", "price": 304.18, "volume": 32430463, "fetched_at": "2026-03-23T14:49:30"},
    {"symbol": "TSLA", "price": 384.05, "volume": 61144022, "fetched_at": "2026-03-23T14:49:30"},
    {"symbol": "MSFT", "price": 385.54, "volume": 33573022, "fetched_at": "2026-03-23T14:49:30"},
    {"symbol": "NVDA", "price": 177.57, "volume": 174151150, "fetched_at": "2026-03-23T14:49:30"}
  ]
}
```

## Run Spark Batch Job
```bash
# Processes data from PostgreSQL into Bronze/Silver/Gold Delta Lake layers
python spark/batch_job.py
```

## Project Structure
```
stock-market-data-platform/
├── kafka/
│   ├── producer.py        # Fetches stock prices → sends to Kafka
│   ├── consumer.py        # Reads Kafka → saves to PostgreSQL
│   └── Dockerfile
├── spark/
│   └── batch_job.py       # Batch ETL → Delta Lake lakehouse
├── flink/
│   └── alerts_job.sql     # Real-time stream processing
├── api/
│   ├── main.py            # FastAPI endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml     # Full stack orchestration
└── README.md
```

## Stocks Tracked

| Symbol | Company |
|---|---|
| AAPL | Apple Inc. |
| GOOGL | Alphabet (Google) |
| TSLA | Tesla Inc. |
| MSFT | Microsoft Corp. |
| NVDA | NVIDIA Corp. |

## What I Learned

- Designing **event-driven architectures** with Kafka producers and consumers
- Implementing **lakehouse patterns** (Bronze/Silver/Gold) with Apache Spark and Delta Lake
- Building **fault-tolerant pipelines** where data is never lost even if consumers go offline
- Containerizing **multi-service applications** with Docker Compose
- Serving data through **production-grade REST APIs** with FastAPI