# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EPROCItem(scrapy.Item):
    kode_paket= scrapy.Field()
    nama_paket= scrapy.Field()
    deskripsi_paket= scrapy.Field()
    nilai_kontrak= scrapy.Field()
    instansi= scrapy.Field()
    HPS= scrapy.Field()
    pass
