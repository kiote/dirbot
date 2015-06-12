# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector

from dirbot.items import Apartment


class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["moscow.thelocals.ru"]
    start_urls = [
        "http://moscow.thelocals.ru/rooms#/?page=1&search[min_price]=3750&search[max_price]=40000&search[only_rooms]=false&search[animals_allowed]=false&search[lat_min]=55.259962662285524&search[lat_max]=56.070317310814076&search[lng_min]=37.164561266992855&search[lng_max]=38.09977244863348&order=date",
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        # mb it's better to have a href regexp here
        apartments = sel.xpath('//div[@class="items"]//a')
        items = []

        for apartment in apartments:
            item = Apartment()
            apartment_sel = Selector(text=apartment.extract())
            item['url'] = apartment_sel.xpath('//a/@href').extract()
            item['time'] = apartment_sel.xpath('//span[@class="catalog-item-time"]//text()').extract()
            item['title'] = apartment_sel.xpath('//div[@class="title"]//text()').extract()
            item['image'] = apartment_sel.xpath('//img/@src').extract()
            item['rooms'] = apartment_sel.xpath('(//div[@class="catalog-item-stats-item-value"])[1]//text()').extract()
            item['area'] = apartment_sel.xpath('(//div[@class="catalog-item-stats-item-value"])[2]//text()').extract()
            item['price'] = apartment_sel.xpath('(//div[@class="catalog-item-stats-item-value"])[3]//text()').extract()
            item['metro_station'] = apartment_sel.xpath('(//span)[last()]//text()').extract()
            items.append(item)
        return items
