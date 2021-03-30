import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from peoplescommunitybank.items import Article


class peoplescommunitybankSpider(scrapy.Spider):
    name = 'peoplescommunitybank'
    start_urls = ['https://www.peoplescommunitybank.com/blog/']

    def parse(self, response):
        links = response.xpath('//a[@class="elementor-post__read-more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@id="post-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
