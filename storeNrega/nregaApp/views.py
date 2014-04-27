# Create your views here.
import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum

from nregaApp.models import State, District, Block, Panchayat, PanchayatData
import sys



def index(request):
	return 0

def panchayats(request,code_):
	block_ = Block.objects.get(code = code_)
	Panchayats = Panchayat.objects.filter(block = block_)
	admStateJSON = json.dumps({p.code: p.name.title() for p in Panchayats})
	return HttpResponse(admStateJSON, content_type='application/json')

def dataretrive(request):
	attr_0 = {'registrations':1,
			'works':2}
	col_map = {'unit': 'attribute_1', 'category': 'attribute_2', 'gender':'attribute_2', 'type': 'attribute_1', 'progress': 'attribute_2'}
	reverseMap = [
			#all indexing starts with 1, 0s are left for unfilled cols as default values, hence the 'null's to shift all indices
			'null',
			{
				'name': 'registrations', 
				'attribute_1': ['null','Households','Workers'],
				'attribute_2': ['null','SC','ST','Others','Women']
				},
			{
				'name': 'Work Distribution',
				'attribute_1':[
					'null',
					'Rural Connectivity',
					'Flood Control',
					'Water Conservation And Water Harversting',
					'Renovation Of Traditional Water Bodies',
					'Drought Proofing',
					'Irrigation Canal',
					'Irrigation Facilities To Sc/St/IAY/LR',
					'Land Development',
					'Other Work',
					'Rajiv Gandhi Seva Kendra',
					'Coastal Areas',
					'Rural Drinking Water',
					'Fisheries',
					'Rural Sanitation'] ,
				'attribute_2':[
					'null',
					'Completed',
					'In Progress/Suspended',
					'Approved but Not In Progress',
					'Proposed but Not Approved']
				}
			]


	#return HttpResponse(json.dumps(request.GET), content_type='application/json')
	#do existential checks for input parameters
	if request.is_ajax():
		query = request.GET
		querySet = PanchayatData.objects.all()
		kwargs = { '{0}_code'.format(query['admLevel']):query['code']}
		querySet=querySet.filter(**kwargs)

		for filterString in query.getlist('filters[]'):
			attributeValPair = filterString.split(':')
			#at some point introduce the need for generic lookup (for eg for attribute_0 too)
			kwargs = { '{0}'.format(col_map[attributeValPair[0]]):reverseMap[attr_0[query['table']]][col_map[attributeValPair[0]]].index(attributeValPair[1])}
			querySet=querySet.filter(**kwargs)
		values = querySet.filter(attribute_0 = attr_0[query['table']]).values(col_map[query['s1']], col_map[query['s2']]).annotate(aggr_data = Sum('data')).order_by(col_map[query['s1']])

		
		#single col specific. Needs to change sooner or later
		series = []
		for attrValue in query.getlist('s2a[]'):
			kwargs = { '{0}'.format(col_map[query['s2']]):reverseMap[attr_0[query['table']]][col_map[query['s2']]].index(attrValue)}
			filteredvalues=values.filter(**kwargs)
			series.append(
					{
						'name': attrValue,
						'data': list(filteredvalues.values_list('aggr_data',flat = True))})

		#vlist = values.filter(col_map[query['s1']], col_map[query['s2']],'aggr_data')
		#vlist = values.values_list(flat = True);
		jsonResponse = json.dumps(series)
		return HttpResponse(jsonResponse, content_type='application/json')
	else:
		return HttpResponse("Post error")

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
	stateSet = State.objects.filter()
	admState = {}
	for state_ in stateSet:
		districtSet = District.objects.filter(state = state_)
		admDistrict = {}
		for district_ in districtSet:
			blockSet = Block.objects.filter(district = district_)
			admBlock = {}
			for block_ in blockSet:
				if(PanchayatData.objects.filter(block_code=block_.code).exists()):
					admBlock[block_.code] = [block_.name.title()]
				
			if(PanchayatData.objects.filter(district_code=district_.code).exists()):
				admDistrict[district_.code] = [district_.name.title(), admBlock]
		if(PanchayatData.objects.filter(state_code=state_.code).exists()):
			admState[state_.code] = [state_.name.title() , admDistrict]
	context = {'adm': admState}
	return render(request, 'dashboard.html', context)
