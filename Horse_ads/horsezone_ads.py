import scrapy
from ..items import HorseAdsItem


class HorsezoneSpider(scrapy.Spider):
    name = 'HZ_ads'

    start_urls = [
        'https://horsezone.com.au/category/196/Horses.html',
        'https://horsezone.com.au/category/197/Stallions_at_Stud.html'
    ]

    # output format
    custom_settings = {'FEED_URI': "HZ_ad_data.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):
        ad_links = response.css('div.title h3 a')
        yield from response.follow_all(ad_links, callback=self.parse_ad)

        # scrape all ad data
        try:
            next_page = response.css('ul.pagination li a')[-1].attrib['href']
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        except:
            pass

    def parse_ad(self, response):
        for item in response.css('div.main'):
            webpage = response.css('title').get()
            title = response.css('.listing_title::text').get()

            try:
                sold = item.xpath('.//div[@class="listing_title"]/img/@src').get()
            except:
                sold = ''

            listing_id = item.xpath('.//div[contains(@style,"display: inline; font-size: 0.6em")]/text()').get()
            num_views = item.xpath('.//span[@class="times-viewed"]/text()').get()
            seller_id = response.css('.seller_username a::text').get()
            extra_question = item.css('.question strong::text').get()
            extra_response = item.css('.answer::text').get()
            stallion_extras = item.xpath('.//div[@id="checkbox"]/ul/li/text()').getall()
            text = item.css('.table.table-condensed.table-hover').get()
            info_label1 = item.css('.label::text')[0].get()
            info_value1 = item.css('.value::text')[1].get()
            info_label2 = item.css('.label::text')[1].get()
            info_value2 = item.css('.value::text')[2].get()
            info_label3 = item.css('.label::text')[2].get()
            info_value3 = item.css('.value::text')[3].get()
            info_label4 = item.css('.label::text')[3].get()
            info_value4 = item.css('.value::text')[4].get()

            try:
                info_label5 = item.css('.label::text')[4].get()
            except:
                info_label5 = ''

            try:
                info_value5 = item.css('.value::text')[5].get()
            except:
                info_value5 = ''

            try:
                info_label6 = item.css('.label::text')[5].get()
            except:
                info_label6 = ''

            try:
                info_value6 = item.css('.value::text')[6].get()
            except:
                info_value6 = ''

            try:
                info_label7 = item.css('.label::text')[6].get()
            except:
                info_label7 = ''

            try:
                info_value7 = item.css('.value::text')[7].get()
            except:
                info_value7 = ''

            try:
                info_label8 = item.css('.label::text')[7].get()
            except:
                info_label8 = ''

            try:
                info_value8 = item.css('.value::text')[8].get()
            except:
                info_value8 = ''

            try:
                info_label9 = item.css('.label::text')[8].get()
            except:
                info_label9 = ''

            items = HorseAdsItem()
            
            items['webpage'] = webpage
            items['title'] = title
            items['sold'] = sold
            items['listing_id'] = listing_id
            items['num_views'] = num_views
            items['seller_id'] = seller_id
            items['text'] = text
            items['extra_question'] = extra_question
            items['extra_response'] = extra_response
            items['stallion_extras'] = stallion_extras
            items['info_label1'] = info_label1
            items['info_value1'] = info_value1
            items['info_label2'] = info_label2
            items['info_value2'] = info_value2
            items['info_label3'] = info_label3
            items['info_value3'] = info_value3
            items['info_label4'] = info_label4
            items['info_value4'] = info_value4
            items['info_label5'] = info_label5
            items['info_value5'] = info_value5
            items['info_label6'] = info_label6
            items['info_value6'] = info_value6
            items['info_label7'] = info_label7
            items['info_value7'] = info_value7
            items['info_label8'] = info_label8
            items['info_value8'] = info_value8
            items['info_label9'] = info_label9

            yield items
