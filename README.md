# Stock Market Data Platform

A production-style data engineering platform that ingests, processes, 
and serves real-time stock market data.

## Architecture
```
Yahoo Finance → Kafka → PostgreSQL → FastAPI
                    ↓
                 Spark
                    ↓
              Delta Lakehouse
           (Bronze/Silver/Gold)
```

## Tech Stack

| Component | Technology |
|---|---|
| Data Ingestion | Apache Kafka |
| Stream Processing | Apache Flink |
| Batch Processing | Apache Spark |
| Storage | PostgreSQL + Delta Lake + MinIO |
| API | FastAPI |
| Containerization | Docker + Docker Compose |

## Services

| Service | Port | Description |
|---|---|---|
| FastAPI | 8000 | REST API |
| Flink Dashboard | 8081 | Job monitoring |
| MinIO | 9001 | Object storage UI |
| Kafka | 9092 | Message broker |
| PostgreSQL | 5433 | Database |

## How to Run
```bash
docker compose up -d
```

## API Endpoints

| Endpoint | Description |
|---|---|
| GET /prices | Latest price for all stocks |
| GET /prices/{symbol} | Price history for one stock |
| GET /stats | Platform statistics |
| GET /alerts | Price alerts |
| GET /docs | Interactive API docs |

## Run Spark Batch Job
```bash
python spark/batch_job.py
```

## Stocks Tracked

AAPL, GOOGL, TSLA, MSFT, NVDA