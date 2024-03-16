import os
import sys
import scrapy


sys.path.append("..")
from pymongo import MongoClient


class Msc3cpoSpider(scrapy.Spider):
    name = "Msc3cpoSpider"
    allowed_domains = ["www.cnmv.es"]
    start_urls = ["https://www.cnmv.es/Portal/Consultas/MostrarListados.aspx?id=18"]

    def __init__(self, *args, **kwargs):
        super(Msc3cpoSpider, self).__init__(*args, **kwargs)

        # get host from environment variable or use default
        host = os.environ.get("MONGODB_HOST", "localhost")
        db = os.environ.get("MONGODB_DATABASE", "sicavs")
        port = int(os.environ.get("MONGODB_PORT", 27017))
        self.client = MongoClient(host, port)
        self.db = self.client[db]
        self.collection = self.db["data"]

    def parse(self, response):
        sicavs = response.css("li.blocks-single")

        for sicav in sicavs:
            relative_url = sicav.css("ul li a").attrib.get("href")
            if relative_url:
                absolute_url = response.urljoin(relative_url)
                yield scrapy.Request(absolute_url, callback=self.parse_sicav_details)

        # Extract the active page and last page
        active_page_str = response.css("span.PagActivaTXT::text").get()

        if len(sicavs) == 0:
            self.logger.warning(
                f"No sicavs found on page {active_page_str}. Moving on..."
            )

        next_link = self.construct_next_page_url(response)

        if next_link:
            self.logger.info("⏭️ Next page: %s", next_link)
            yield scrapy.Request(next_link, callback=self.parse)

    def construct_next_page_url(self, response):
        return response.xpath(
            "//li[span[@class='active']]/following-sibling::li[1]/a/@href"
        ).get()

    def parse_sicav_details(self, response):
        nombre_sicav = response.css("#ctl00_ContentPrincipal_lblSubtitulo::text").get()
        tabla_principal = response.css("#ctl00_ContentPrincipal_gridDatos")

        nombre = nombre_sicav

        num_registro_oficial = response.css(
            'td[data-th="Nº Registro oficial"]::text'
        ).get()

        fecha_registro_oficial = response.css(
            'td[data-th="Fecha registro oficial"]::text'
        ).get()

        domicilio = response.css('td[data-th="Domicilio"]::text').get()

        # For capital_social_inicial

        capital_social_inicial = self.parseFloat(
            response, 'td[data-th="Capital social inicial"]::text'
        )

        # For capital_maximo_estatutario
        capital_maximo_estatutario = self.parseFloat(
            response, 'td[data-th="Capital máximo estatutario"]::text'
        )

        isin = response.css('td[data-th="ISIN"] a::text').get()

        fecha_ultimo_folleto = response.css(
            'td[data-th="Fecha último folleto"]::text'
        ).get()

        sicav_data = {
            "nombre": nombre,
            "num_registro_oficial": num_registro_oficial,
            "fecha_registro_oficial": fecha_registro_oficial,
            "domicilio": domicilio,
            "capitales": {
                "inicial": capital_social_inicial,
                "maximo_estatutario": capital_maximo_estatutario,
            },
            "ISIN": isin,
        }
        folleto = {
            "fecha": fecha_ultimo_folleto,
            "domicilio": domicilio,
            "capitales": {
                "inicial": capital_social_inicial,
                "maximo_estatutario": capital_maximo_estatutario,
            },
        }
        current_sicav = self.collection.find_one(
            {"num_registro_oficial": num_registro_oficial}
        )

        if not current_sicav or any(
            [
                current_sicav.get("domicilio") != domicilio,
                current_sicav.get("capitales", {}).get("inicial")
                != capital_social_inicial,
                current_sicav.get("capitales", {}).get("maximo_estatutario")
                != capital_maximo_estatutario,
            ]
        ):
            try:
                self.collection.update_one(
                    {"num_registro_oficial": num_registro_oficial},
                    {"$set": sicav_data, "$addToSet": {"folletos": folleto}},
                    upsert=True,
                )
            except Exception as e:
                self.logger.error(f"Failed to insert sicav data into MongoDB: {e}")

        else:
            try:
                self.collection.update_one(
                    {"num_registro_oficial": num_registro_oficial},
                    {"$set": sicav_data},
                    upsert=True,
                )
            except Exception as e:
                self.logger.error(f"Failed to insert sicav data into MongoDB: {e}")

        yield {"sicav_data": sicav_data, "folleto": folleto}

    def closed(self, reason):
        self.client.close()

    def parseFloat(self, response, selector):
        text = response.css(selector).get()
        if text:
            text = text.replace(",", "").replace(" €", "").strip()
            return float(text)

        else:
            return None
