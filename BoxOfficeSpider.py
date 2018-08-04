import scrapy

class BoxOfficeSpider(scrapy.Spider):

    name = "box_office_all_time_domestic"
    start_urls = [
        'https://www.boxofficemojo.com/alltime/domestic.htm?page=0',
    ]

    def parse(self, response):
        results_table = '/html/body/div/div[3]/div[2]/table[2]/tr/td[1]/center/table[2]/tr[2]/td/table/tr'

        if len(response.xpath(results_table)) > 1:
            for result in response.xpath(results_table):
                    yield {
                        'rank': result.xpath('td[1]/font/text()').extract_first(),
                        'title': result.xpath('td[2]/font/a/b/text()').extract_first(),
                        'studio': result.xpath('td[3]/font/a/text()').extract_first(),
                        'amount': result.xpath('td[4]/font/b/text()').extract_first(),
                    }

            url_parts = response.url.split('=')
            url_parts[1] = str(int(url_parts[1]) +  1)

            yield response.follow("=".join(url_parts), self.parse)
        else:
            yield
