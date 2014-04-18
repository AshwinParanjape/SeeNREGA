from django.core.management.base import BaseCommand, CommandError
from nregaApp.models import State, District, Block, Panchayat
import json
import gzip
import lzw
import cStringIO

class Command(BaseCommand):
	args = ''
	help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):
		stateSet = State.objects.all()
		admState = {}
		for state_ in stateSet:
			districtSet = District.objects.filter(state = state_)
			admDistrict = {}
			for district_ in districtSet:
				blockSet = Block.objects.filter(district = district_)
				admBlock = {}
				for block_ in blockSet:
					#panchayatSet = Panchayat.objects.filter(block = block_)
					#admBlock[block_.name.title()] = [p.name.title() for p in panchayatSet]
					admBlock[block_.code] = [block_.name.title()]
					
				admDistrict[district_.code] = [district_.name.title(), admBlock]
			admState[state_.code] = [state_.name.title() , admDistrict]
		admStateJSON = json.dumps(admState)
		handle1=open('nregaApp/static/preAggregatedData/adm.json','w')
		handle1.write(admStateJSON)
		handle1.close()
		oldBytes = lzw.readbytes('nregaApp/static/preAggregatedData/adm.json')
		lessbytes = lzw.compress(oldBytes)
		for b in lessbytes:
			lzw.writebytes('nregaApp/static/preAggregatedData/adm.lzw',b)
