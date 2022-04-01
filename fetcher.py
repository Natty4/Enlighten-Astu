import requests

# baseUrl = "http://127.0.0.1:8000"
baseUrl = "https://enlightenapi.herokuapp.com"

def recored_new_user(obj):

    url = f"{baseUrl}/api/tguser"
    data = obj
    respons = requests.post(url, data=data)
    if respons.status_code != 201:
        return False
    return respons


def upload_file(obj, typ):
    url = f"{baseUrl}/api/{typ}"
    data = obj
    respons = requests.post(url, data=data)
    return respons


def get_courses():
    url = f"{baseUrl}/api/cms"
    resp = requests.get(url)
    if resp.status_code == 404:
        return False
    data = resp.json()["CourseMaterial-Info"]
    courses = data
    return courses


def get_courses_of(data, semester):
    Data = data
    courses = {}
    for course in Data:
        if str(course["semester"]) == str(semester):
            courses[course["course_code"]] = course
    return courses


def get_semesters(campus):
    url = f"{baseUrl}/api/{campus}/semesters"
    data = requests.get(url)
    if data.status_code == 404:
        return False
    resp = data.json()["Semester-Info"]
    respons = []
    for dt in resp:
        semester = {}
        semester["name"] = dt["name"]
        semester["semes_number"] = dt["semes_number"]
        semester["campus"] = dt["campus"]
        semester["school_in_this_semes"] = dt["school_in_this_semes"]

        respons.append(semester)

    return respons


def get_departments(dep):
    url = f"{baseUrl}/api/{dep}"
    data = requests.get(url)
    if data.status_code == 404:
        return False
    resp = data.json()["Department-Info"]
    respons = []
    for dt in resp:
        department = {}
        department["id"] = dt["id"]
        department["short_name"] = dt["short_name"]
        department["name"] = dt["name"]

        respons.append(department)
    return respons


def get_departments_by_semester(sem):
    url = f"{baseUrl}/api/semesters/{sem}"
    data = requests.get(url)
    if data.status_code == 404:
        return False
    resp = data.json()["Semester-Info"]
    respons = []
    for school in resp["school_in_this_semes"]:
        for department in school["department"]:

            departments = {}
            departments["id"] = department["id"]
            departments["short_name"] = department["short_name"]
            departments["name"] = department["name"]
            departments["school"] = school["name"]
            respons.append(departments)
    return respons


def get_all_by_sem_and_dep(sem, dep):
    url = f"{baseUrl}/api/cms/{sem}/{dep}"
    data = requests.get(url)
    if data.status_code == 404:
        return False
    resp = data.json()["CourseMaterial-Info"]
    respons = []
    for courses in resp:
        av = {}
        course = {}
        course["course_id"] = courses["id"]
        course["course_name"] = courses["course_name"]
        course["course_code"] = courses["course_code"]
        course["course_description"] = courses["course_description"]
        course["semester"] = courses["semester"]
        course["department"] = courses["department"]
        course["created_by"] = courses["created_by"]
        if courses["ppts"]:
            av["PPT"] = len(courses["ppts"])
        if courses["pdfs"]:
            av["PDF"] = len(courses["pdfs"])
        if courses["books"]:
            av["Book"] = len(courses["books"])
        course["available"] = av

        respons.append(course)

    return respons


import re
import ast


def get_course_tg(ccode):
    url = f"{baseUrl}/api/cms/{ccode}"
    data = requests.get(url)
    if data.status_code == 404:
        return False
    resp = data.json()["CourseMaterial-Info"]
    respons = {}
    ava = data.json()["available File Format"]
    aval = {}
    filesid = {}
    filespath = {}
    filetitle = {}
    filecontributor = {}
    for a in ava:
        aval[a] = len(resp[a.lower() + "s"])

    for i in aval:
        fid = []
        fpath = []
        ftitle = []
        fcontributor = []
        j = resp[i.lower() + "s"]
        for file in j:
            fcont = ast.literal_eval(re.search('({.+})', file['contributors']).group(0)).get('first_name', 'anonymous')
            fid.append(file["tg_file_id"])
            fpath.append(file["tg_file_url"])
            ftitle.append(file['title'])
            fcontributor.append(fcont)
        filesid[i] = fid
        filespath[i] = fpath
        filetitle['file_title'] = ftitle
        filecontributor['tg_contributors'] = fcontributor
    course = {}

    course["course_id"] = resp["id"]
    course["course_name"] = resp["course_name"]
    course["course_code"] = resp["course_code"]
    course["course_description"] = resp["course_description"]
    course["semester"] = resp["semester"]
    course["department"] = resp["department"]
    course["created_by"] = resp["created_by"]
    course["ava"] = aval
    course["filesid"] = filesid
    course["filespath"] = filespath
    course["filetitle"] = filetitle
    course["filecontributor"] = filecontributor
    respons[resp["course_name"]] = course

    return respons


def get_fast(ccode):
    url = f"{baseUrl}/api/cms/{ccode}"
    print(url)
    data = requests.get(url)
    if data.status_code == 404:
        return False
    resp = data.json()["CourseMaterial-Info"]
    respons = {}
    ava = data.json()["available File Format"]
    aval = {}
    filesid = {}
    filespath = {}
    filetitle = {}
    filecontributor = {}
    for a in ava:
        aval[a] = len(resp[a.lower() + "s"])

    for i in aval:
        fid = []
        fpath = []
        ftitle = []
        fcontributor = []
        j = resp[i.lower() + "s"]
        for file in j:
            fcont = ast.literal_eval(re.search('({.+})', file['contributors']).group(0)).get('first_name', 'anonymous')
            fid.append(file["tg_file_id"])
            fpath.append(file["tg_file_url"])
            ftitle.append(file['title'])
            fcontributor.append(fcont)
        filesid[i] = fid
        filespath[i] = fpath
        filetitle['file_title'] = ftitle
        filecontributor['tg_contributors'] = fcontributor
    course = {}
    course["course_id"] = resp["id"]
    course["course_name"] = resp["course_name"]
    course["course_code"] = resp["course_code"]
    course["course_description"] = resp["course_description"]
    course["semester"] = resp["semester"]
    course["department"] = resp["department"]
    course["created_by"] = resp["created_by"]
    course["ava"] = aval
    course["filesid"] = filesid
    course["filespath"] = filespath
    course["filetitle"] = filetitle
    course["filecontributor"] = filecontributor
    respons[resp["course_name"]] = course

    return respons
