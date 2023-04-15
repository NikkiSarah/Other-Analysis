# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HorseAdsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    webpage = scrapy.Field()
    title = scrapy.Field()
    sold = scrapy.Field()
    listing_id = scrapy.Field()
    num_views = scrapy.Field()
    seller_id = scrapy.Field()
    text = scrapy.Field()
    extra_question = scrapy.Field()
    extra_response = scrapy.Field()
    stallion_extras = scrapy.Field()
    info_label1 = scrapy.Field()
    info_value1 = scrapy.Field()
    info_label2 = scrapy.Field()
    info_value2 = scrapy.Field()
    info_label3 = scrapy.Field()
    info_value3 = scrapy.Field()
    info_label4 = scrapy.Field()
    info_value4 = scrapy.Field()
    info_label5 = scrapy.Field()
    info_value5 = scrapy.Field()
    info_label6 = scrapy.Field()
    info_value6 = scrapy.Field()
    info_label7 = scrapy.Field()
    info_value7 = scrapy.Field()
    info_label8 = scrapy.Field()
    info_value8 = scrapy.Field()
    info_label9 = scrapy.Field()

class HorseAdsItem2(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hyperlink = scrapy.Field()
    webpage = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    num_views = scrapy.Field()
    breed_location = scrapy.Field()
    height = scrapy.Field()
    age_sex_rider_service = scrapy.Field()
    listing_id = scrapy.Field()
    num_photos = scrapy.Field()
    text = scrapy.Field()
    featured_ad = scrapy.Field()
    discipline = scrapy.Field()
    sold = scrapy.Field()
