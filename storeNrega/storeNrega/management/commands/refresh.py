from django.core.management.base import BaseCommand, CommandError
from polls.models import Poll

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
					#admBlock[block_.name] = [p.name for p in panchayatSet]
					admBlock[block_.name]=[]
				admDistrict[district_.name] = admBlock
			admState[state_.name] = admDistrict
		admStateJSON = json.dumps(admState)
		handle1=open('nregaApp/static/preAggregatedData/adm.json','r+')
		handle1.write(admStateJson)
		handle1.close()
