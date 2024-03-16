# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlanksScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    nombre = scrapy.Field()
    NumRegistroOficial = scrapy.Field()
    FechaRegistroOficial = scrapy.Field()
    Domicilio = scrapy.Field()
    CapitalSocialIncial = scrapy.Field()
    CapitalMaximoEstatutario = scrapy.Field()
    isin = scrapy.Field()
    FechaUltimoFolleto = scrapy.Field()
