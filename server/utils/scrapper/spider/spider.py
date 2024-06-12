import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class DynamicSpider(scrapy.Spider):
    name = 'dynamic_spider'
    allowed_domains = ['lpse.pu.go.id']
    start_urls = ['https://lpse.bogorkab.go.id/eproc4/lelang']
    items = []
    
    def __init__(self):
        super(DynamicSpider, self).__init__()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        # Locate and interact with the selection input
        select_xpath = "/html/body/div[6]/div/div/div/div/div[1]/div[1]/div[1]/div/label/select"

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, select_xpath))
        )

        select_element = self.driver.find_element(By.XPATH, select_xpath)
        select = Select(select_element)
        select.select_by_index(2)  # Assuming options are 0-based index then pick 100

        # Wait for 5 seconds to let the page load dynamically
        time.sleep(5)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr"))
        )

        rows = self.driver.find_elements(By.XPATH, "/html/body/div[6]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr")
        main_window = self.driver.current_window_handle

        for row in rows:
            kode_tender = row.find_element(By.XPATH, "./td[1]").text
            detail_url = f"https://lpse.bogorkab.go.id/eproc4/lelang/{kode_tender}/pengumumanlelang"
            self.driver.execute_script(f"window.open('{detail_url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr[1]/td/strong"))
            )

            item = self.extract_detail_page()
            self.items.append(item)

            self.driver.close()
            self.driver.switch_to.window(main_window)

        self.driver.quit()
        return self.items
    
    def extract_detail_page(self):
        item = {}

        def get_text_or_default(xpath, default=""):
            try:
                return self.driver.find_element(By.XPATH, xpath).text
            except:
                return default

        item['kode_tender'] = get_text_or_default("//tr[1]/td/strong")
        item['nama_tender'] = get_text_or_default("//tr[2]/td/strong")
        item['tanggal_pembuatan'] = get_text_or_default("//tr[th[contains(text(), 'Tanggal Pembuatan')]]/td[1]")
        item['jenis_pengadaan'] = get_text_or_default("//tr[th[contains(text(), 'Jenis Pengadaan')]]/td[1]")
        item['instansi'] = get_text_or_default("//tr[th[contains(text(), 'K/L/PD/Instansi Lainnya')]]/td[1]")
        item['satuan_kerja'] = get_text_or_default("//tr[th[contains(text(), 'Satuan Kerja')]]/td[1]")
        item['tahun_anggaran'] = get_text_or_default("//tr[th[contains(text(), 'Tahun Anggaran')]]/td[1]")
        item['nilai_pagu_paket'] = get_text_or_default("//tr[th[contains(text(), 'Nilai Pagu Paket')]]/td[1]")
        item['nilai_hps_paket'] = get_text_or_default("//tr[th[contains(text(), 'Nilai HPS Paket')]]/td[2]")
        item['jenis_kontrak'] = get_text_or_default("//tr[th[contains(text(), 'Jenis Kontrak')]]/td[1]")
        item['lokasi_pengerjaan'] = get_text_or_default("//tr[th[contains(text(), 'Lokasi Pekerjaan')]]/td[1]/ul/li")
        item['syarat_kualifikasi'] = get_text_or_default("//tr[th[contains(text(), 'Syarat Kualifikasi')]]/td[1]")
        item['peserta_tender'] = get_text_or_default("//tr[th[contains(text(), 'Peserta Tender')]]/td[1]")

        return item

    def closed(self, reason):
        self.driver.quit()
