# Create your views here.
import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from nregaApp.models import State, District, Block, Panchayat


def index(request):
	return 0
def admJSON(request):
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
	return HttpResponse(admStateJSON, content_type='application/json')

def query(request):
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
	context = {'adm': admState}
	return render(request, 'dashboard.html', context)
