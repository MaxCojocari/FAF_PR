import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_links(url, max_page_num):
    if not re.search(r'\?page', url):
        url += '?page=1'

    page_nr_limit = get_pagination_limit(get_response(url))
    
    if page_nr_limit and max_page_num > page_nr_limit:
        max_page_num = int(page_nr_limit)
    
    if max_page_num == 0:
        return
    
    file_path = 'in_class.txt'
    if os.path.exists(file_path):
        os.remove(file_path)

    while True:
        response = get_response(url)
        page_nr = int(url.split('page=')[1])

        if page_nr > max_page_num:
            return

        get_links_to_products(response)
        url = get_next_url_from_pagination(response)
        
        if not url:
            return 

        continue

def get_links_to_products(response, url_base='https://999.md'):
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    with open('in_class.txt', 'a') as file:
        for link in links:
            href = link.get('href')
            if href and re.match(r'/ro/\d+', href):
                # print(urljoin(url_base, href))
                file.write(urljoin(url_base, href) + '\n')
              

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
    scrape_links(start_url, max_page_num=10)
