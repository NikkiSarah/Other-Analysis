import pandas as pd
import scrapy

class CRANSpider(scrapy.Spider):
    name = 'CRAN'

    data = pd.read_excel("R packages.xlsx")
    URL_list = data['URL'].to_list()

    start_urls = URL_list

    # output format
    custom_settings = {'FEED_URI': "CRAN_package_data.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):
        # CRAN package page data to extract
        yield {
            'webpage': response.css("samp::text").get(),
            'package_title': response.css("h2::text").get(),
            'description': response.css("p::text").getall()
        }
