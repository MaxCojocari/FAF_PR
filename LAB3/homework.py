import requests
import json
from bs4 import BeautifulSoup
from unidecode import unidecode

class PageScrapper:
    def __init__(self, url):
        self.url = url
        self.response = self.make_get_request(url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.product_name = ""
        self.content_description = ""
        self.seller_id = ""
        self.price = {}
        self.region = ""
        self.tel = ""
        self.general = {}
        self.safety = []
        self.features = {}
        self.comfort = []

    @staticmethod
    def make_get_request(url):
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Error: {str(e)}")

        return response

    def set_product_name(self):
        element = self.soup.find('header', class_='adPage__header').find('h1', itemprop='name')
        self.product_name = element.text

    def set_content_description(self):
        element = self.soup.find('div', class_='adPage__content__description grid_18', itemprop="description")
        self.content_description = unidecode(element.text)

    def set_seller_id(self):
        element = self.soup.find('a', class_='adPage__aside__stats__owner__login')
        self.seller_id = element.text.strip()

    def set_price(self):
        amount = self.soup.find('span', class_='adPage__content__price-feature__prices__price__value').get('content')
        currency = self.soup.find('span', class_="adPage__content__price-feature__prices__price__currency").get('content')
        self.price = {"amount": amount, "currency": currency}

    def set_region(self):
        elements = self.soup.find('dl', class_="adPage__content__region grid_18").find_all('dd')
        country = elements[0].find('meta').get('content')
        locality = elements[1].find('meta').get('content')
        self.region = {"country": unidecode(country), "locality": unidecode(locality)}

    def set_tel_nr(self):
        element = self.soup.find('dl', class_="js-phone-number adPage__content__phone is-hidden grid_18").find('a', href=True).get('href')
        self.tel = element.replace("tel:", "")

    def get_general_info(self, className):
        ul_elements = self.soup.find('div', class_=className).find_all('ul')
        h2_elements = self.soup.find('div', class_=className).find_all('h2')

        data = {}
        
        if len(h2_elements) == 1:
            first_section_name = h2_elements[0].text.strip().lower()
            data[first_section_name] = {}

        if len(h2_elements) == 2:
            first_section_name = h2_elements[0].text.strip().lower()
            second_section_name = h2_elements[1].text.strip().lower()
            data[first_section_name] = {}
            data[second_section_name] = []

        for ul_element in ul_elements:
            for li in ul_element.find_all('li', class_='m-value'):
                
                key_element = li.find('span', itemprop='name')
                value_element = li.find('span', itemprop='value')
                
                if first_section_name:
                    if key_element and value_element:
                        key = unidecode(key_element.text.strip().lower())
                        value = unidecode(value_element.text.strip())
                        data[first_section_name][key] = value

            for li in ul_element.find_all('li', class_='m-no_value'):
                key_element = li.find('span', itemprop='name')
                
                if second_section_name:
                    if key_element:
                        key = unidecode(key_element.text.strip().lower())
                        data[second_section_name].append(key)
        
        return data
    
    def set_general(self):
        info = self.get_general_info('adPage__content__features__col grid_9 suffix_1')
        if info.get('general') is not None:
            self.general = info['general']
    
    def set_safety(self):
        info1 = self.get_general_info('adPage__content__features__col grid_7 suffix_1')
        info2 = self.get_general_info('adPage__content__features__col grid_9 suffix_1')
        if info1.get('securitate') is not None:
            self.safety = info1['securitate']
        if info2.get('securitate') is not None:
            self.safety = info2['securitate']

    def set_features(self):
        info = self.get_general_info('adPage__content__features__col grid_7 suffix_1')
        if info.get('particularități') is not None:
            self.features = info['particularități']
    
    def set_comfort(self):
        info1 = self.get_general_info('adPage__content__features__col grid_7 suffix_1')
        info2 = self.get_general_info('adPage__content__features__col grid_9 suffix_1')
        if info1.get('confort') is not None:
            self.comfort = info1['confort']
        if info2.get('confort') is not None:
            self.comfort = info2['confort']

    def scrap(self):
        self.set_product_name()
        self.set_content_description()
        self.set_seller_id()
        self.set_price()
        self.set_region()
        self.set_tel_nr()
        self.set_general()
        self.set_safety()
        self.set_features()
        self.set_comfort()
        return self

    def to_json(self):
        return {
            "product_name": self.product_name,
            "content_description": self.content_description,
            "seller_id": self.seller_id,
            "price": self.price,
            "region": self.region,
            "tel": self.tel,
            "general": self.general,
            "safety": self.safety,
            "feature": self.features,
            "comfort": self.comfort
        }



if __name__ == "__main__":
    base_url = "https://999.md/ro/83927441"
    pageScrapper = PageScrapper(base_url)
    data = pageScrapper.scrap().to_json()

    file_name = "homework.json"
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file)
