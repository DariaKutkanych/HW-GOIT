import scrapy

class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):

        authors = []
        for quote in response.xpath("/html//div[@class='quote']"):
    
            quote_info = {
                "keywords": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract(),
                "quote": quote.xpath("span[@class='text']/text()").get()[1:-1],
                "author_ref": f'{self.start_urls[0]}{quote.xpath("span/a/@href").get()}'
            }
            author = quote.xpath("span/small/text()").get()
            if author not in authors:
                authors.append(author)
                yield response.follow(quote.xpath("span/a/@href").get(), callback=self.parse_author, cb_kwargs=quote_info)
            else:
                yield quote_info
            
        next_link = response.xpath("//li[@class='next']/a/@href").get()

        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
    
    def parse_author(self, response, **kwargs):
        
        yield {**kwargs,
              "born": response.xpath("/html//div[@class='author-details']/p/span[@class='author-born-date']/text()").get()
              }
