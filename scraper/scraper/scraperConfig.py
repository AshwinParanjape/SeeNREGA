from urlparse import *
global_start_urls = [ "http://nrega.nic.in/Netnrega/stHome.aspx" ]
district_extractor = '//th/*[contains(.,"District")]/../../following-sibling::tr//a'
block_extractor = '//th/*[contains(.,"Block")]/../../following-sibling::tr//a'
panchayat_extractor = '//tr[contains(.,"Panchayats")]/following-sibling::tr//a'
benificiary_breakup_link_text = 'Category, BPL Family, RSBY, Small Marginal Farmer Status'
blockDataConfig = {'Category Gender Wise Household Registered Under MGNREGA' :
		{'name' : 2, 'registered_households_SC':3, 'registered_households_ST':4, 'registered_households_Others':5,
			'registered_workers_SC':7,'registered_workers_ST':8,'registered_workers_Others':9,'registered_workers_Women':11}}
#strings used in query urls. Uppercase letters are converted to lowercase before comparison
#state_name = ['state_name']
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
