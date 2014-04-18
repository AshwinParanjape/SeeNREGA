#from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class State(models.Model):
	code = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)
	
class District(models.Model):
	state = models.ForeignKey(State)
	code = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)

class Block(models.Model):
	district = models.ForeignKey(District)
	code = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)
	link = models.CharField(max_length = 2048)

class Panchayat(models.Model):
	block = models.ForeignKey(Block)
	code = models.BigIntegerField(primary_key = True)
	name = models.CharField(max_length = 100, null = True)
	alternateName = models.CharField(max_length = 100, null = True)
	registered_households_SC = models.IntegerField(null = True)
	registered_households_ST = models.IntegerField(null = True)
	registered_households_Others = models.IntegerField(null = True)
	registered_workers_SC = models.IntegerField(null = True)
	registered_workers_ST = models.IntegerField(null = True)
	registered_workers_Others = models.IntegerField(null = True)
	registered_workers_Women = models.IntegerField(null = True)
	benificiary_household_RSBY = models.IntegerField(null = True)
	benificiary_household_Small_Farmer = models.IntegerField(null = True)
	benificiary_household_Marginal_Farmer = models.IntegerField(null = True)
	benificiary_household_LR = models.IntegerField(null = True)
	benificiary_household_IAY = models.IntegerField(null = True)
	benificiary_household_SC = models.IntegerField(null = True)
	benificiary_household_ST = models.IntegerField(null = True)
	benificiary_household_Others = models.IntegerField(null = True)
	benificiary_household_Minority = models.IntegerField(null = True)
	benificiary_household_FRA = models.IntegerField(null = True)

class PanchayatData(models.Model):
	state_code = models.IntegerField()
	district_code = models.IntegerField()
	block_code = models.IntegerField()
	panchayat_code = models.BigIntegerField()
	year = models.IntegerField()
	attribute_0 = models.SmallIntegerField()
	attribute_1 = models.SmallIntegerField()
	attribute_2 = models.SmallIntegerField()
	attribute_3 = models.SmallIntegerField()
	data = models.FloatField()

class BlockBorder(models.Model):
	id_0 = models.IntegerField()
	iso = models.CharField('3 Digit ISO', max_length=3)
	name_0 = models.CharField(max_length = 75)
	id_1 = models.IntegerField()
	name_1 = models.CharField(max_length = 75)
	id_2 = models.IntegerField()
	name_2 = models.CharField(max_length = 75)
	id_3 = models.IntegerField()
	name_3 = models.CharField(max_length = 75)
	nl_name_3 = models.CharField(max_length = 75)
	varname_3 = models.CharField(max_length = 100)
	type_3 = models.CharField(max_length = 50)
	engtype_3 = models.CharField(max_length = 50)
	mpoly = models.MultiPolygonField()
	objects = models.GeoManager()
	# Returns the string representation of the model.
	def __str__(self):              # __unicode__ on Python 2
		return self.name_3+", "+self.name_2+", "+self.name_1


