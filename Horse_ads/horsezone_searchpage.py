import scrapy


class HorsezoneSpider(scrapy.Spider):
    name = 'HZ_searchpage'

    start_urls = [
        'https://horsezone.com.au/category/196/Horses.html',
        'https://horsezone.com.au/category/197/Stallions_at_Stud.html'
    ]

    # output format
    custom_settings = {'FEED_URI': "HZ_searchpage_data.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):
        # search-page data to extract
        for ad in response.css('article.listing.clearfix'):
            yield {
                'webpage': response.css('title')[1].get(),
                'hyperlink': ad.xpath('.//h3/a/@href').get(),
                'title': ad.xpath('.//h3/a/text()').get(),
                'price': ad.xpath('.//span[@class="price"]/text()').get(),
                'excerpt': ad.xpath('.//p[contains(@class, "description")]/a/text()').get(),
                'disciplines': ad.xpath('.//p[@class="optional_1"]/a/text()[2]').get(),
                'location': ad.xpath('.//div[@class="legend-location"]/p/a/text()[2]').get(),
                'sold': ad.xpath('.//div[@class="title"]/a/img/@src').get()
            }

        # scrape all search-page data
        try:
            next_page = response.css('ul.pagination li a')[-1].attrib['href']
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        except:
            pass
