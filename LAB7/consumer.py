import pika
import os
from dotenv import load_dotenv
from product_scrapper import ProductScrapper

load_dotenv('./rabbitmq.env')

QUEUE = 'product_urls'
USERNAME=os.getenv('RABBITMQ_DEFAULT_USER')
PASSWORD=os.getenv('RABBITMQ_DEFAULT_PASS')

credentials = pika.PlainCredentials(USERNAME, PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue=QUEUE, durable=False)

def main():
    def callback(ch, method, properties, body):
        url = body.decode()
        print(f"Crawling: {url}")

        pageScrapper = ProductScrapper(url)
        data = pageScrapper.scrap().to_json()
        print(data)
        
        # Acknowledge the url_in queue indicating successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set the prefetch count to 1 to ensure that the consumer processes one message at a time
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()

if __name__ == '__main__':
    main()
