import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dynamic_scraper.items import EPROCItem
import json

class DynamicSpider(scrapy.Spider):
    name = 'dynamic_spider'
    allowed_domains = ['lpse.pu.go.id']
    start_urls = ['https://lpse.pu.go.id/eproc4/lelang']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')  # Added to avoid running as root error in some environments
        chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
        self.driver = webdriver.Chrome(options=chrome_options)
        self.cookies = []

    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr"))
        )

        self.cookies = self.driver.get_cookies()

        rows = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr")

        for row in rows:
            kode_tender = row.find_element(By.XPATH, "./td[1]").text
            detail_url = f"https://lpse.pu.go.id/eproc4/lelang/{kode_tender}/pengumumanlelang"
            yield scrapy.Request(detail_url, callback=self.parse_detail, cookies=self.get_scrapy_cookies(), headers=self.get_custom_headers())

        self.driver.quit()

    def parse_detail(self, response, **kwargs):
        self.driver.get(response.url)
        """STILL ERORRRRRRR"""
        kode_tender= self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/table/tbody/tr[1]/td/strong').text
        print(kode_tender)


    def get_scrapy_cookies(self):
        """Convert Selenium cookies to Scrapy cookies."""
        cookies = {}
        for cookie in self.cookies:
            cookies[cookie['name']] = cookie['value']
        return cookies

    def get_custom_headers(self):
        """Return custom headers mimicking a regular browser request."""
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8,ja;q=0.7',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Referer': 'https://lpse.pu.go.id/eproc4/lelang'
        }

    def closed(self, reason):
        self.driver.quit()

