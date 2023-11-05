import pika
import os
import threading
from dotenv import load_dotenv
from pymongo import MongoClient
from pdp_scraper import ProductPageScraper

load_dotenv('./rabbitmq.env')
QUEUE_NAME = 'product_urls'
RABBITMQ_USERNAME = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS')
credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)

load_dotenv('./.env')
MONGO_USERNAME=os.getenv('MONGO_USERNAME')
MONGO_PASSWORD=os.getenv('MONGO_PASSWORD')
MONGO_DATABASE=os.getenv('MONGO_DATABASE')
MONGO_HOST=os.getenv('MONGO_HOST')
MONGO_URI = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}'
COLLECTION_NAME = 'lab7_collection'

# Establish a connection to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[COLLECTION_NAME]


def consume():
    # Establish a connection to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
    channel = connection.channel()

    # Connect to a queue
    channel.queue_declare(queue=QUEUE_NAME, durable=False)

    def callback(ch, method, properties, body):
        url = body.decode()
        print(f"Crawling: {url}")

        pageScraper = ProductPageScraper(url)
        data = pageScraper.scrap().to_json()
        print(data)
        collection.insert_one(data)
        
        # Acknowledge the url_in queue indicating successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set the prefetch count to 1 to ensure that the consumer processes one message at a time
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()

def main():
    num_threads = 8

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=consume)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()