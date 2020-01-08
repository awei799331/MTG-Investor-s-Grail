import scrapy

class priceSpider(scrapy.Spider):
    name = "goldfishSpider"
    allowed_domains = ["https://www.mtggoldfish.com"]
    start_urls = [
        "https://www.mtggoldfish.com/price/Throne+of+Eldraine/The+Great+Henge#paper"
    ]

    def start_requests(self):
        for each in self.start_urls:
            yield scrapy.Request(each, self.parse)

    def parse(self, response):
        yeet = response.xpath("//script[contains(., 'MTGGoldfishDygraph.bindTabs')]/text()").extract()
        with open('your_file.txt', 'w') as f:
            for item in yeet:
                f.write("%s\n" % item)
        yield {
            "data":yeet
        }