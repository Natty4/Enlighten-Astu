import requests


# baseUrl = 'http://127.0.0.1:8000'
baseUrl = 'https://enlightenapi.herokuapp.com'

def recored_new_user(obj):

	# obj = {
	#     "username": "lol",
	#     "first_name": "Lol",
	#     "last_name": "LoL"
	# }
	url = f'{baseUrl}/api/tguser'
	data = obj
	respons = requests.post(url, data = data)
	return respons

def upload_file(obj, typ):
	url = f'{baseUrl}/api/{typ}'
	# obj = {
	#     "cm":cm,
	#     "tg_file_id": "2020",
	#     "tg_file_url": "url/from/tg/somthing",
	#     "title": ""

	# }
	data = obj
	respons = requests.post(url, data = data)
	return respons

def get_semesters(campus):
	url = f'{baseUrl}/api/{campus}/semesters'
	data = requests.get(url)
	if data.status_code == 404:
		return False
	resp = data.json()['Semester-Info']
	respons = []
	for dt in resp:
		semester = {}
		semester['name'] = dt['name']
		semester['semes_number'] = dt['semes_number']
		semester['campus'] = dt['campus']
		semester['school_in_this_semes'] = dt['school_in_this_semes']

		respons.append(semester)

	return respons
def get_departments(dep):
	url = f'{baseUrl}/api/{dep}'
	data = requests.get(url)
	if data.status_code == 404:
		return False
	resp = data.json()['Department-Info']
	respons = []
	for dt in resp:
		department = {}
		department['id'] = dt['id']
		department['short_name'] = dt['short_name']
		department['name'] = dt['name']

		respons.append(department)
	return respons
def get_departments_by_semester(sem):
	url = f'{baseUrl}/api/semesters/{sem}'
	data = requests.get(url)
	if data.status_code == 404:
		return False
	resp = data.json()['Semester-Info']
	respons = []
	for school in resp['school_in_this_semes']:
		for department in school['department']:

			departments = {}
			departments['id'] = department['id'] 
			departments['short_name'] = department['short_name'] 
			departments['name'] = department['name'] 
			departments['school'] = school['name']
			respons.append(departments)
	return respons
def get_all_by_sem_and_dep(sem, dep):
	url = f'{baseUrl}/api/cms/{sem}/{dep}'
	data = requests.get(url)
	if data.status_code == 404:
		return False
	resp = data.json()['CourseMaterial-Info']
	respons = []
	for courses in resp:
		av = {}
		course = {}
		course['course_id'] = courses['id']
		course['course_name'] = courses['course_name']
		course['course_code'] = courses['course_code']
		course['course_description'] = courses['course_description']
		course['semester'] = courses['semester']
		course['department'] = courses['department']
		course['created_by'] = courses['created_by']
		if courses['ppts']:
			av['PPT'] = len(courses['ppts'])
		if courses['pdfs']:
			av['PDF'] = len(courses['pdfs'])
		if courses['books']:
			av['Book'] = len(courses['books'])
		course['available'] = av

		respons.append(course)

	return respons

# def get_course(sem, dep, ccode):
# 	url = f'{baseUrl}/api/cms/{sem}/{dep}/{ccode}'
# 	print(url)
# 	data = requests.get(url)
# 	# print(data)
# 	if data.status_code == 404:
# 		return False
# 	resp = data.json()['CourseMaterial-Info']
# 	respons = {}
# 	ava = data.json()['available File Format']
# 	aval = {}
# 	path = {}
# 	for a in ava:
# 	    aval[a]=len(resp[a.lower() + 's'])

# 	for i in aval:
# 		url = []
# 		j = resp[i.lower() + 's']
# 		for file in j:
# 			url.append(baseUrl + file[i.lower()])
# 		path[i] = url
# 	course = {}
# 	course['course_name'] = resp['course_name']
# 	course['course_code'] = resp['course_code']
# 	course['course_description'] = resp['course_description']
# 	course['semester'] = resp['semester']
# 	course['department'] = resp['department']
# 	course['created_by'] = resp['created_by']
# 	course['ava'] = aval
# 	course['files'] = path
# 	respons[resp['course_name']] = course

# 	# print(respons)
# 	return respons

def get_course_tg(sem, dep, ccode):
	url = f'{baseUrl}/api/cms/{sem}/{dep}/{ccode}'
# 	print(url)
	data = requests.get(url)
	# print(data)
	if data.status_code == 404:
		return False
	resp = data.json()['CourseMaterial-Info']
	respons = {}
	ava = data.json()['available File Format']
	aval = {}
	path = {}
	for a in ava:
	    aval[a]=len(resp[a.lower() + 's'])
	
	for i in aval:
		fid = []
		j = resp[i.lower() + 's']
		for file in j:
			# url.append(baseUrl + file[i.lower()])
# 			print(file, "File__________")
			fid.append(file['tg_file_id'])

		path[i] = fid
	course = {}
	course['course_name'] = resp['course_name']
	course['course_code'] = resp['course_code']
	course['course_description'] = resp['course_description']
	course['semester'] = resp['semester']
	course['department'] = resp['department']
	course['created_by'] = resp['created_by']
	course['ava'] = aval
	course['files'] = path
	respons[resp['course_name']] = course

	# print(respons)
	return respons

def get_fast(ccode):
	url = f'{baseUrl}/api/cms/{ccode}'
# 	print(url)
	data = requests.get(url)
	if data.status_code == 404:
		return False
	else:
		resp = data.json()['CourseMaterial-Info']
		# print(resp)
		respons = {}
		ava = data.json()['available File Format']
		aval = {}
		path = {}
		for a in ava:
		    aval[a]=len(resp[a.lower() + 's'])
		for i in aval:
			url = []
			j = resp[i.lower() + 's']
			for file in j:
				url.append(baseUrl + file[i.lower()])
			path[i] = url
		course = {}
		course['course_name'] = resp['course_name']
		course['course_code'] = resp['course_code']
		course['course_description'] = resp['course_description']
		course['semester'] = resp['semester']
		course['department'] = resp['department']
		course['created_by'] = resp['created_by']
		course['ava'] = aval
		course['files'] = path
		respons[resp['course_name']] = course

		# print(respons)
		return respons
