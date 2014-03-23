from django.db import models

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

