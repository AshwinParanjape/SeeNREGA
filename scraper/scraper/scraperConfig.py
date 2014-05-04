from urlparse import *
global_start_urls = [ "http://nrega.nic.in/Netnrega/stHome.aspx" ]
district_extractor = '//th/*[contains(.,"District")]/../../following-sibling::tr//a'
block_extractor = '//th/*[contains(.,"Block")]/../../following-sibling::tr//a'
panchayat_extractor = '//tr[contains(.,"Panchayats")]/following-sibling::tr//a'
benificiary_breakup_link_text = 'Category, BPL Family, RSBY, Small Marginal Farmer Status'


#attribute0 - table nums
registered_data = 1
number_of_works = 2

#attribute 1 - registered_data
registered_households = 1
registered_workers = 2
#attribute 2 - registered_data
SC = 1
ST = 2
Others = 3
Women = 4

#attribute 1 - number_of_works
rural_connectivity = 1 
flood_control = 2 
water_conservation_and_water_harversting = 3
renovation_of_traditional_water_bodies = 4
drought_proofing = 5
irrigation_canals = 6
irrigation_facilities_to_sc_st_iay_lr = 7
land_development = 8
other_works = 9
rajiv_gandhi_seva_kendra = 10
coastal_areas = 11
rural_drinking_water = 12
fisheries = 13
rural_sanitation = 14

#attribute 2 - number_of_works
completed = 1
in_progress_or_suspended = 2
approved_not_progressed = 3
proposed_not_approved = 4

#def getAttributeNum(x,l):
#	if x in l
#		return x
#	else return 0

blockDataConfig = {
'Category Gender Wise Household Registered Under MGNREGA' :
			[ registered_data, 2,
				
				{
				3: [registered_households,SC],
				4: [registered_households,ST],
				5: [registered_households,Others],
				7: [registered_workers,SC],
				8: [registered_workers,ST],
				9: [registered_workers,Others],
				11: [registered_workers,Women],
			} ],

			'Works under different category/status':
			[number_of_works, 2, 
			{
				3: [rural_connectivity,completed],
				4: [rural_connectivity,in_progress_or_suspended],
				5: [rural_connectivity,approved_not_progressed],
				6: [rural_connectivity,proposed_not_approved],
				7: [flood_control,completed],
				8: [flood_control,in_progress_or_suspended],
				9: [flood_control,approved_not_progressed],
				10: [flood_control,proposed_not_approved],
				11: [water_conservation_and_water_harversting,completed],
				12: [water_conservation_and_water_harversting,in_progress_or_suspended],
				13: [water_conservation_and_water_harversting,approved_not_progressed],
				14: [water_conservation_and_water_harversting,proposed_not_approved],
				15:[renovation_of_traditional_water_bodies,completed],
				16:[renovation_of_traditional_water_bodies,in_progress_or_suspended],
				17:[renovation_of_traditional_water_bodies,approved_not_progressed],
				18:[renovation_of_traditional_water_bodies,proposed_not_approved],
				19:[drought_proofing,completed],
				20:[drought_proofing,in_progress_or_suspended],
				21:[drought_proofing,approved_not_progressed],
				22:[drought_proofing,proposed_not_approved],
				23:[irrigation_canals,completed],
				24:[irrigation_canals,in_progress_or_suspended],
				25:[irrigation_canals,approved_not_progressed],
				26:[irrigation_canals,proposed_not_approved],
				27:[irrigation_facilities_to_sc_st_iay_lr,completed],
				28:[irrigation_facilities_to_sc_st_iay_lr,in_progress_or_suspended],
				29:[irrigation_facilities_to_sc_st_iay_lr,approved_not_progressed],
				30:[irrigation_facilities_to_sc_st_iay_lr,proposed_not_approved],
				31:[land_development,completed],
				32:[land_development,in_progress_or_suspended],
				33:[land_development,approved_not_progressed],
				34:[land_development,proposed_not_approved],
				35:[other_works,completed],
				36:[other_works,in_progress_or_suspended],
				37:[other_works,approved_not_progressed],
				38:[other_works,proposed_not_approved],
				39:[rajiv_gandhi_seva_kendra,completed],
				40:[rajiv_gandhi_seva_kendra,in_progress_or_suspended],
				41:[rajiv_gandhi_seva_kendra,approved_not_progressed],
				42:[rajiv_gandhi_seva_kendra,proposed_not_approved],
				43:[coastal_areas,completed],
				44:[coastal_areas,in_progress_or_suspended],
				45:[coastal_areas,approved_not_progressed],
				46:[coastal_areas,proposed_not_approved],
				47:[rural_drinking_water,completed],
				48:[rural_drinking_water,in_progress_or_suspended],
				49:[rural_drinking_water,approved_not_progressed],
				50:[rural_drinking_water,proposed_not_approved],
				51:[fisheries,completed],
				52:[fisheries,in_progress_or_suspended],
				53:[fisheries,approved_not_progressed],
				54:[fisheries,proposed_not_approved],
				55:[rural_sanitation,completed],
				56:[rural_sanitation,in_progress_or_suspended],
				57:[rural_sanitation,approved_not_progressed],
				58:[rural_sanitation,proposed_not_approved],
		}],
	}
#strings used in query urls. Uppercase letters are converted to lowercase before comparison
#state_name = [state_name']
#state_code = ['state_code']
#district_name = ['district_name']
#district_code = ['district_code']
#block_name = ['block_name']
#block_code = ['block_code']
#panchayat_name = ['panchayat_name']
#panchayat_code = ['panchayat_code']
#year = ['finyear','fin_year']

state_name = 'state_name'
state_code = 'state_code'
district_name = 'district_name'
district_code = 'district_code'
block_name = 'block_name'
block_code = 'block_code'
panchayat_name = 'panchayat_name'
panchayat_code = 'panchayat_code'
year = 'finyear'

def parse_url(url):
	query_string = urlparse(url).query
	query_dict = parse_qs(query_string)
	#convert to lowercase for comparison
	query_dict = {key.lower(): value[0] for key,value in query_dict.items()}
	return query_dict

links = [
			'Category Gender Wise Household Registered Under MGNREGA',
			'Total No. of Aadhaar Nos. Entered for MGNREGA',
			'Age Wise Registered and Employed Persons',
			'BPL Families Registered, Applicants with A/C No., Photos Uploaded',
			'Category, BPL Family, RSBY, Small Marginal Farmer Status',
			'E-Muster Roll and Wagelist',
			'Executing Agency Wise Muster Roll Detail',
			'Employment Status',
			'Progress Report',
			'Employment Provided Period wise',
			'Households Completed 100 days in Financial Year',
			'Person Engaged in Work Category Irrigation Facilities to SC/ST BPL Families',
			'New HouseHold Joined MGNREGA',
			'Employment Provided to Disabled Persons',
			'Gender wise wage analysis of employment provided on work',
			'Employment Pattern During the year',
			'SC ST Employment Status',
			'Work Category Wise Employment Provided',
			'HouseHold Worked For At least 15 days in MGNREGA',
			'Households worked more than 100 days',
			'Households worked less than 15 days',
			'Household provided employment with specified no. of days',
			'Household/Worker without Family/Worker Photo',
			'Works under different category/status',
			'Work Status',
			'Work Execution Level Analysis',
			'Expenditure analysis of Ongoing works',
			'Spill Over Works',
			'Progress of Work Execution',
			'Suspended Work',
			'No. Of Works Under Convergence Entered in MIS',
			'Yearly Work Completion Rate',
			'Bharat Nirman Rajeev Gandhi Sewa Kendra',
			'BNRGSK Additional information',
			'Photos of Works since inception(Before start,During execution and completed)',
			'Status of Photos of Work Uploaded in MIS',
			'Assets Created',
			'Details of Assets Created',
			'Fund Transfer Statement and Expenditure',
			'Financial Statement',
			'Outlays & Outcomes',
			'Funds and Expenditure Summary',
			'Average wage paid pattern during the year',
			'Per Day Wise Expenditure of Gram Panchayats',
			'Per Day Wise Administrative Expenditure of Gram Panchayats',
			'Implementing Wise Financial Statement of Gram Panchayats',
			'Labour ,Material Ratio Analysis',
			'Administrative Expenditure Report',
			'Expenditure on works',
			'Available Fund at Each Level'
	]
