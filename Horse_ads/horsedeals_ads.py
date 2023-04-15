import pandas as pd
import scrapy
from ..items import HorseAdsItem2

url_series = pd.read_csv("D:\Libraries\Documents\Data Science\PycharmProjects\horse_ads\\url_series.csv", index_col=0)
url_list = url_series.iloc[:,0].tolist()


class HorseDealsSpider(scrapy.Spider):
    name = 'HD_ads'

    start_urls = url_list

    # output format
    custom_settings = {'FEED_URI': "HD_ad_data.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):
        for item in response.css('article.product-details'):
            hyperlink = response.request
            listing_id = item.css('.product__contact div::attr(advert-id)').get()
            num_photos = item.css('.carousel__count-total::text').get()
            num_views = item.css('.views span::text').get()
            text = item.css('.product__description p').getall()
            title = item.xpath('.//h1[@itemprop="name"]/text()').get()
            webpage = response.css('title::text').get()

            try:
                price = item.css('.price span::text').get()
            except:
                price = ''
                continue

            try:
                featured = item.css('.is-featured::text').get()
            except:
                featured = ''
                continue

            try:
                breed_location = item.css('.product__attribute dd a::text').getall()
            except:
                breed_location = ''
                continue

            try:
                height = item.css('.product__attribute[itemprop="height"] dd::text').get()
            except:
                height = ''
                continue

            try:
                age_sex_rider_service = item.css('.product__attribute dd::text').getall()
            except:
                age_sex_rider_service = ''
                continue

            try:
                discipline = item.css('.product__discipline dd a::text').getall()
            except:
                discipline = ''
                continue

            try:
                sold = item.css('.product__flag.is-sold::text').get()
            except:
                sold = ''
                continue

            items = HorseAdsItem2()

            items['hyperlink'] = hyperlink
            items['webpage'] = webpage
            items['title'] = title
            items['price'] = price
            items['num_views'] = num_views
            items['breed_location'] = breed_location
            items['height'] = height
            items['age_sex_rider_service'] = age_sex_rider_service
            items['listing_id'] = listing_id
            items['num_photos'] = num_photos
            items['text'] = text
            items['featured_ad'] = featured
            items['discipline'] = discipline
            items['sold'] = sold

            yield items
