# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector

from dirbot.items import Apartment

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["moscow.thelocals.ru"]
    start_urls = [
        "http://moscow.thelocals.ru/rooms#/?page=1&search[min_price]=3750&search[max_price]=40000&search[only_rooms]=false&search[animals_allowed]=false&search[lat_min]=55.259962662285524&search[lat_max]=56.070317310814076&search[lng_min]=37.164561266992855&search[lng_max]=38.09977244863348&order=date",
    ]

    def _save_item(self, item, selector, field_name, path):
        try:
            item[field_name] = selector.xpath(path).extract()[0]
        except IndexError:
            item[field_name] = ''

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
            self._save_item(item, apartment_sel, 'url', '//a/@href')
            self._save_item(item, apartment_sel, 'time', '//span[@class="catalog-item-time"]//text()')
            self._save_item(item, apartment_sel, 'title', '//div[@class="title"]//text()')
            self._save_item(item, apartment_sel, 'image', '//img/@src')
            self._save_item(item, apartment_sel, 'rooms', '(//div[@class="catalog-item-stats-item-value"])[1]//text()')
            self._save_item(item, apartment_sel, 'area', '(//div[@class="catalog-item-stats-item-value"])[2]//text()')
            self._save_item(item, apartment_sel, 'price', '(//div[@class="catalog-item-stats-item-value"])[3]//text()')
            self._save_item(item, apartment_sel, 'metro_station', '(//span)[last()]//text()')
            items.append(item)
        return items
