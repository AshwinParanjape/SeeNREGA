from django.core.management.base import BaseCommand, CommandError
from nregaApp.models import State, District, Block, Panchayat, PanchayatData
import json

class Command(BaseCommand):
	args = ''
	help = 'runs a one time query to find the which adms have data'
	print 'ha'
	def handle(self, *args, **options):
		stateSet = State.objects.all()
		admState = {}
		existingStates = PanchayatData.objects.values('state_code').annotate().values_list('state_code', flat=True);
		for stateCode in existingStates:
			print 'state:'+str(stateCode)
			admDistrict = {}
			existingDistricts = PanchayatData.objects.filter(state_code = stateCode).values('district_code').annotate().values_list('district_code', flat=True);
			for districtCode in existingDistricts:
				print 'district:'+str(districtCode)
				admBlock = {}
				existingBlocks = PanchayatData.objects.filter(district_code = districtCode).values('block_code').annotate().values_list('block_code', flat=True);

				for blockCode in existingBlocks:
					print 'block:'+str(blockCode)
					block_ = Block.objects.get(code = blockCode)
					admBlock[block_.code] = [block_.name.title()]
				district_ = District.objects.get(code = districtCode)
				admDistrict[district_.code] = [district_.name.title(), admBlock]
			state_ = State.objects.get(code = stateCode)
			admState[state_.code] = [state_.name.title() , admDistrict]
		admStateJSON = json.dumps(admState)
		handle1=open('nregaApp/static/preAggregatedData/adm.json','w')
		handle1.write(admStateJSON)
		handle1.close()
