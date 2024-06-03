# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EPROCItem(scrapy.Item):
    kode_tender= scrapy.Field()
    nama_tender= scrapy.Field()
    tanggal_pembuatan= scrapy.Field()
    jenis_pengadaan= scrapy.Field()
    instansi= scrapy.Field()
    satuan_kerja= scrapy.Field()
    tahun_anggaran= scrapy.Field()
    nilai_pagu_paket= scrapy.Field()
    nilai_hps_paket= scrapy.Field()
    jenis_kontrak= scrapy.Field()
    lokasi_pengerjaan= scrapy.Field()
    syarat_kualifikasi= scrapy.Field()
    peserta_tender= scrapy.Field()
    pass
