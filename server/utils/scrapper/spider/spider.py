import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class DynamicSpider(scrapy.Spider):
    name = 'dynamic_spider'
    allowed_domains = ['lpse.jakarta.go.id']
    start_urls = ['https://lpse.jakarta.go.id/eproc4']
    items = []

    def __init__(self):
        super().__init__()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div/div[3]/div/div/div[2]/table/tbody/tr[contains(@class, 'Jasa_Konsultansi_Badan_Usaha_Non_Konstruksi')]//a"))
        )

        types = [
            'Pengadaan_Barang', 'Jasa_Konsultansi_Badan_Usaha_Non_Konstruksi', 'Pekerjaan_Konstruksi',
            'Jasa_Lainnya', 'Jasa_Konsultansi_Perorangan_Non_Konstruksi', 'Jasa_Konsultansi_Badan_Usaha_Konstruksi',
            'Jasa_Konsultansi_Perorangan_Konstruksi', 'Pekerjaan_Konstruksi_Terintegrasi'
        ]
        anchors = []

        for type in types:
            data = self.driver.find_elements(By.XPATH, f"//*[@id='main']/div/div/div[3]/div/div/div[2]/table/tbody/tr[contains(@class, '{type}')]//a")
            if data:
                anchors.extend(data)
        
        main_window = self.driver.current_window_handle

        for anchor in anchors:
            detail_url = anchor.get_attribute('href')
            self.driver.execute_script(f"window.open('{detail_url}', '_blank');")
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
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

        with open('server/utils/scrapper/spider/sbu.json', 'r') as sbu_file:
            sbu_list = json.load(sbu_file)

        with open('server/utils/scrapper/spider/kbli.json', 'r') as kbli_file:
            kbli_list = json.load(kbli_file)

        syarat_kualifikasi_text = item['syarat_kualifikasi']
        item['kode_sbu'] = next((sbu for sbu in sbu_list if sbu in syarat_kualifikasi_text), 'N/A')
        item['kode_kbli'] = next((kbli for kbli in kbli_list if kbli in syarat_kualifikasi_text), 'N/A')

        del item['syarat_kualifikasi']

        # Navigate to the steps detail page
        detail_url = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr[6]/td/a").get_attribute('href')
        self.driver.execute_script(f"window.open('{detail_url}', '_blank');")
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 2)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Scrape the data from the table step
        item['tahapan_tender'] = []
        rows = self.driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr")

        for i, row in enumerate(rows, start=2):  # Starting from 2 to match tr[2], tr[3], etc.
            tahap = get_text_or_default(f"/html/body/div[2]/div/div/table/tbody/tr[{i}]/td[2]", default="")
            mulai = get_text_or_default(f"/html/body/div[2]/div/div/table/tbody/tr[{i}]/td[3]", default="")
            sampai = get_text_or_default(f"/html/body/div[2]/div/div/table/tbody/tr[{i}]/td[4]", default="")
    
            if tahap or mulai or sampai:  # Only append if at least one value is not empty
                item['tahapan_tender'].append({
                    'tahap': tahap,
                    'mulai': mulai,
                    'sampai': sampai
                })

        return item

    def closed(self, reason):
        self.driver.quit()
