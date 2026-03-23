import json
import time
import os
import logging
import yfinance as yf
from kafka import KafkaProducer
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
STOCKS = ["AAPL", "GOOGL", "TSLA", "MSFT", "NVDA"]
TOPIC = "stock-prices"

def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def fetch_and_send(producer):
    logging.info("Fetching stock prices...")
    for symbol in STOCKS:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.fast_info.last_price
            volume = ticker.fast_info.three_month_average_volume

            message = {
                "symbol": symbol,
                "price": price,
                "volume": volume,
                "timestamp": datetime.now().isoformat()
            }

            producer.send(TOPIC, message)
            logging.info(f"Sent: {symbol} ${price:.2f}")

        except Exception as e:
            logging.error(f"Failed {symbol}: {e}")
    
    producer.flush()
    logging.info("All prices sent to Kafka")

if __name__ == "__main__":
    producer = create_producer()

    # Create topic first
    logging.info("Starting producer - fetching every 60 seconds...")
    while True:
        fetch_and_send(producer)
        time.sleep(60)