import re
import os
import pika
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv('./rabbitmq.env')

QUEUE_NAME = 'product_urls'
RABBITMQ_USERNAME = os.getenv('RABBITMQ_DEFAULT_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS')
credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=False)
channel.queue_purge(queue=QUEUE_NAME)

seen = set()

def scrape_links(url, max_page_num):
    page_nr_limit = get_pagination_limit(get_response(url))
    
    if page_nr_limit and max_page_num > page_nr_limit:
        max_page_num = int(page_nr_limit)
    
    if max_page_num == 0:
        return

    while True:
        response = get_response(url)
        page_nr = 0
        url_frag = url.split('page=')
        
        if len(url_frag) > 1:
            page_nr = int(url_frag[1])

        if page_nr != 0 and page_nr > max_page_num:
            return

        get_links_to_products(response)
        url = get_next_url_from_pagination(response)
        
        if url is None:
            return  


def get_links_to_products(response, url_base='https://999.md'):
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        href = link.get('href')
        
        if href and re.match(r'/ro/\d+', href):
            full_url = urljoin(url_base, href)
            
            if full_url not in seen:
                seen.add(full_url)
                print(full_url)
                channel.basic_publish(
                    exchange='', 
                    routing_key='product_urls', 
                    body=full_url, 
                    properties=pika.BasicProperties(delivery_mode=1) # Non-persistent message
                )

def get_next_url_from_pagination(response, url_base='https://999.md'):
    soup = BeautifulSoup(response.text, 'html.parser')
    
    current_li = soup.find('li', class_='current')
    next_li = current_li.find_next_sibling('li')

    if next_li:
        next_a = next_li.find('a')
        if next_a:
            href = next_a.get('href')
            return urljoin(url_base, href)
    
    return None

def get_pagination_limit(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    
    fragment = soup.find('li', class_='is-last-page')
    
    if fragment:
        link = fragment.find('a', href=True)
        href = link.get('href')
        return int(href.split('page=')[1])
    
    return None

def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return response

if __name__ == "__main__":
    start_url = "https://999.md/ro/list/transport/cars"
    scrape_links(start_url, 10)