import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from dynamic_scraper.items import EPROCItem
import json

class DynamicSpider(scrapy.Spider):
    name = 'dynamic_spider'
    allowed_domains = ['lpse.pu.go.id']
    start_urls = ['https://lpse.pu.go.id/eproc4/lelang?kategoriId=&tahun=2008&instansiId=&rekanan=&kontrak_status=&kontrak_tipe=']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        # Wait for JavaScript to load
        self.driver.implicitly_wait(10)
        items = []  # Initialize an empty list to collect items

        # Extract data from multiple rows in the table
        rows = self.driver.find_elements("xpath", "/html/body/div[6]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr")
        for row in rows:
            # Extract data from each row
            kode_paket= row.find_element('xpath', "./td[1]").text
            nama_paket = row.find_element("xpath", "./td[2]/p[1]/a").text
            deskripsi_paket= row.find_element('xpath', "./td[2]/p[2]").text
            nilai_kontrak= row.find_element('xpath', "./td[2]/p[3]").text
            instansi= row.find_element('xpath', "./td[3]").text
            hps= row.find_element('xpath', "./td[5]").text
            
            # Create an item and yield it
            item = EPROCItem()
            item['kode_paket'] = kode_paket
            item['nama_paket'] = nama_paket
            item['deskripsi_paket'] = deskripsi_paket
            item['nilai_kontrak'] = nilai_kontrak
            item['instansi'] = instansi
            item['HPS'] = hps

            items.append(item)  # Append each item to the list
            yield item
        # Close the driver
        self.driver.quit()

        with open('2008_output.json', 'w') as f:
            json.dump([dict(item) for item in items], f)
