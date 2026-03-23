import json
import os
import logging
from kafka import KafkaConsumer
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/stocks")

engine = create_engine(DATABASE_URL)



def save_price(symbol, price, volume):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO stock_prices (symbol, price, volume)
            VALUES (:symbol, :price, :volume)
        """), {"symbol": symbol, "price": price, "volume": volume})
        conn.commit()
        logging.info(f"Saved to DB: {symbol} ${price:.2f}")

if __name__ == "__main__":
    logging.info("Starting consumer...")
    consumer = KafkaConsumer(
        "stock-prices",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id="stock-db-consumer",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    for message in consumer:
        data = message.value
        save_price(data["symbol"], data["price"], data["volume"])