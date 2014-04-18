# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from django.db import models
from scrapy.contrib.djangoitem import DjangoItem
from nregaApp.models import State, District, Block, Panchayat, PanchayatData

from scrapy.item import Item, Field

class StateItem(DjangoItem):
	django_model = State

class DistrictItem(DjangoItem):
	django_model = District

class BlockItem(DjangoItem):
	django_model = Block
	
class PanchayatItem(DjangoItem):
	django_model = Panchayat

class PanchayatDataItem(DjangoItem):
	django_model = Panchayat
	
class Dummy(Item):
	dum = Field()
