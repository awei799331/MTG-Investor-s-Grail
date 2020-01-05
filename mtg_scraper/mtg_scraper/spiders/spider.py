import scrapy

class priceSpider(scrapy.Spider):
    name = "goldfishSpider"

    start_urls = [
        "https://www.mtggoldfish.com/price/Throne+of+Eldraine/The+Great+Henge#paper"
    ]

    def parse(self, response):
        yeet = response.xpath("//script[contains(., 'MTGGoldfishDygraph.bindTabs')]/text()")
        print(yeet)
        yield {
            'data':yeet
        }
