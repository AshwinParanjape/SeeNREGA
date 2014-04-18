# Create your views here.
import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse

from nregaApp.models import State, District, Block, Panchayat


def index(request):
	return 0

def panchayats(request,code_):
	block_ = Block.objects.get(code = code_)
	Panchayats = Panchayat.objects.filter(block = block_)
	admStateJSON = json.dumps({p.code: p.name for p in Panchayats})
	return HttpResponse(admStateJSON, content_type='application/json')

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
				admBlock[block_.code] = [block_.name.title()]
				
			admDistrict[district_.code] = [district_.name.title(), admBlock]
		admState[state_.code] = [state_.name.title() , admDistrict]
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
				admBlock[block_.code] = [block_.name.title()]
				
			admDistrict[district_.code] = [district_.name.title(), admBlock]
		admState[state_.code] = [state_.name.title() , admDistrict]
	context = {'adm': admState}
	return render(request, 'dashboard.html', context)
