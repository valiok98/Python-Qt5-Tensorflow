import scrapy

class quotesScraoer(scrapy.Spider):

    name = 'quotes'

    start_urls = [
        'http://quotes.toscrape.com/page/1',
        'http://quotes.toscrape.com/page/2'
    ]

    for url in start_urls:
        pass