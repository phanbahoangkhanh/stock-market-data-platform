import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI(title="Stock Market Data Platform")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/stocks")
engine = create_engine(DATABASE_URL)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                id         SERIAL PRIMARY KEY,
                symbol     TEXT NOT NULL,
                price      FLOAT NOT NULL,
                volume     BIGINT,
                fetched_at TIMESTAMP DEFAULT NOW()
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS stock_alerts (
                id         SERIAL PRIMARY KEY,
                symbol     TEXT NOT NULL,
                message    TEXT NOT NULL,
                price      FLOAT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
        conn.commit()

init_db()

@app.get("/")
def home():
    return {"message": "Stock Market Data Platform is running"}

@app.get("/prices")
def get_latest_prices():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT DISTINCT ON (symbol)
                symbol, price, volume, fetched_at
            FROM stock_prices
            ORDER BY symbol, fetched_at DESC
        """))
        return {"data": [dict(row._mapping) for row in rows]}

@app.get("/prices/{symbol}")
def get_price_history(symbol: str):
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT symbol, price, volume, fetched_at
            FROM stock_prices
            WHERE symbol = :symbol
            ORDER BY fetched_at DESC
            LIMIT 100
        """), {"symbol": symbol.upper()})
        data = [dict(row._mapping) for row in rows]
    if not data:
        return {"error": f"No data found for {symbol}"}
    return {"symbol": symbol.upper(), "total": len(data), "data": data}

@app.get("/alerts")
def get_alerts():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT * FROM stock_alerts
            ORDER BY created_at DESC
            LIMIT 50
        """))
        return {"data": [dict(row._mapping) for row in rows]}

@app.get("/stats")
def get_stats():
    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT
                COUNT(*) as total_records,
                COUNT(DISTINCT symbol) as total_symbols,
                MIN(fetched_at) as first_record,
                MAX(fetched_at) as latest_record
            FROM stock_prices
        """)).fetchone()
    return dict(row._mapping)