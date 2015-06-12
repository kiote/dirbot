# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class Apartment(Item):

    rooms = Field()
    area = Field()
    price = Field()
    title = Field()
    metro_station = Field()
    url = Field()
    time = Field()
    image = Field()
