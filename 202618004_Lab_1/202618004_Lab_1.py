import scrapy
from scrapy.crawler import CrawlerProcess

class BookSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]
    custom_settings = {
        "FEEDS": {
            "books.csv": {
                "format": "csv",
                "overwrite": True
            }
        },
        "LOG_LEVEL": "ERROR"
    }

    def parse(self, response):
        for book in response.css("article.product_pod"):
            href = book.css("h3 a::attr(href)").get()
            yield response.follow(href, callback=self.parse_book)
        current_page = int(response.url.split("page-")[-1].replace(".html", ""))
        if current_page < 5:
            next_page = f"https://books.toscrape.com/catalogue/page-{current_page+1}.html"
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_book(self, response):
        table = {}
        for row in response.css("table.table.table-striped tr"):
            key = row.css("th::text").get()
            value = row.css("td::text").get()
            table[key] = value
        description = response.css("#product_description + p::text").get(default="")
        yield {
            "Title": response.css("div.product_main h1::text").get(),
            "Category": response.css("ul.breadcrumb li:nth-child(3) a::text").get(),
            "Price": response.css("p.price_color::text").get(),
            "Rating": response.css("p.star-rating::attr(class)").get().replace("star-rating ", ""),
            "Availability": " ".join(
                t.strip()
                for t in response.css("p.availability::text").getall()
                if t.strip()
            ),
            "Product Description": description,
            "UPC": table.get("UPC"),
            "Number of Reviews": table.get("Number of reviews"),
            "Product URL": response.url
        }


process = CrawlerProcess()
process.crawl(BookSpider)
process.start()