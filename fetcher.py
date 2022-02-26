import requests

baseUrl = 'https://enlightenapi.herokuapp.com'


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

def get_course(sem, dep, ccode):
	url = f'{baseUrl}/api/cms/{sem}/{dep}/{ccode}'
	data = requests.get(url)
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

def get_fast(ccode):
	url = f'{baseUrl}/api/cms/{ccode}'
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