from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from users.permissions import IsOwnerOrReadOnly
from .models import *
from .serializers import *


class TGUserCreateApiView(APIView):
	queryset = TGUser.objects.all()
	serializer_class = TGUserSerializer

	def post(self, request, format=None):
		serializer = TGUserSerializer(data = request.data)
		if serializer.is_valid(raise_exception = True):
			serializer.save()
			return Response(status = status.HTTP_201_CREATED)
		return Response(status = status.HTTP_400_BAD_REQUEST)


class CourseMaterialListApiView(APIView):

	def get_object(self):
		try:
			if not CourseMaterial.objects.filter(is_active = True):
				raise Http404
			else:
				return CourseMaterial.objects.filter(is_active = True)

		except CourseMaterial.DoesNotExist:
			raise Http404
	def get(self ,request , format = None):

		CourseMaterial = self.get_object()

		serialized_CourseMaterial = CourseMaterialSerializer(CourseMaterial, many = True)

		return Response({ 
							
							"CourseMaterial-Info" : serialized_CourseMaterial.data, 
							"status" : status.HTTP_200_OK
						})


class CourseMaterialFastApiView(APIView):

	def get_object(self, course_code):
		try:
			if not CourseMaterial.objects.filter(is_active = True).get(course_code = course_code):
				raise Http404
			else:
				return CourseMaterial.objects.filter(is_active = True).get(course_code = course_code)

		except CourseMaterial.DoesNotExist:
			raise Http404
	def available_format(self, course_code):
		available_formats = []
		if LecturePPT.objects.filter(cm__course_code = course_code):
			available_formats.append('PPT')

		if LecturePDF.objects.filter(cm__course_code = course_code):
			available_formats.append('PDF')

		if LectureBook.objects.filter(cm__course_code = course_code):
			available_formats.append('Book')
		return available_formats

	def get(self ,request, course_code, format = None):

		CourseMaterial = self.get_object(course_code)
		available_formats = self.available_format(course_code)
		serialized_CourseMaterial = CourseMaterialSerializer(CourseMaterial)

		return Response({ 	"available File Format" : available_formats, 
							"CourseMaterial-Info" : serialized_CourseMaterial.data, 
							"status" : status.HTTP_200_OK
						})




class CourseMaterialListBySemesterDepartmentApiView(APIView):

	def get_object(self, semester, department):
		try:
			if not CourseMaterial.objects.filter(is_active = True, semester = semester, department = department):
				raise Http404
			else:
				return CourseMaterial.objects.filter(is_active = True, semester = semester, department = department)

		except CourseMaterial.DoesNotExist:
			raise Http404
	def get(self ,request, semester, department, format = None):

		CourseMaterial = self.get_object(semester, department)

		serialized_CourseMaterial = CourseMaterialSerializer(CourseMaterial, many = True)

		return Response({ "CourseMaterial-Info" : serialized_CourseMaterial.data, "status" : status.HTTP_200_OK})



class CourseMaterialListByDepartmentApiView(APIView):

	def get_object(self, department):
		try:
			if not CourseMaterial.objects.filter(is_active = True, department__short_name = department):
				raise Http404
			else:
				return CourseMaterial.objects.filter(is_active = True, department__short_name = department)

		except CourseMaterial.DoesNotExist:
			raise Http404
	def get(self ,request, department, format = None):

		CourseMaterial = self.get_object(department)

		serialized_CourseMaterial = CourseMaterialSerializer(CourseMaterial, many = True)

		return Response({ "CourseMaterial-Info" : serialized_CourseMaterial.data, "status" : status.HTTP_200_OK})




class CourseMaterialDetailApiView(APIView):


	def get_object(self, semester, department, course_code,):
		try:
			return CourseMaterial.objects.filter(semester = semester, department = department).get(course_code = course_code)
		except CourseMaterial.DoesNotExist:
			raise Http404
	def available_format(self, course_code):
		available_formats = []
		if LecturePPT.objects.filter(cm__course_code = course_code):
			available_formats.append('PPT')

		if LecturePDF.objects.filter(cm__course_code = course_code):
			available_formats.append('PDF')

		if LectureBook.objects.filter(cm__course_code = course_code):
			available_formats.append('Book')
		return available_formats
	

	def get(self ,request , semester = None, department = None, course_code = None, format = None):
	    
		course_material = self.get_object(semester, department, course_code)
		available_formats = self.available_format(course_code)

		course_ppt = LecturePPT.objects.filter(cm__semester = semester, cm__department = department, cm__course_code = course_code)
		serialized_LecturePPT = PPTSerializer(course_ppt , many = True)
		course_pdf = LecturePDF.objects.filter(cm__semester = semester, cm__department = department, cm__course_code = course_code)
		serialized_LecturePDF = PDFSerializer(course_pdf , many = True)
		course_book = LectureBook.objects.filter(cm__semester = semester, cm__department = department, cm__course_code = course_code)
		serialized_LectureBook = BookSerializer(course_book , many = True)
		##serializing CourseMaterial 
		serialized_courseMaterial = CourseMaterialSerializer(course_material)


		return Response({
			"available File Format" : available_formats, 
			"CourseMaterial-Info" : serialized_courseMaterial.data,
			# "CourseMaterial-PPT" : serialized_LecturePPT.data, 
			# "CourseMaterial-PDF" : serialized_LecturePDF.data, 
			# "CourseMaterial-book" : serialized_LectureBook.data, 
	  
	    })


 

class DepartmentListApiView(APIView):
	serializer_class = DepartmentSerializer

	def get_object(self, school):
		try:
			return Department.objects.filter(school__name = school)
		except Department.DoesNotExist:
			raise Http404

	def get(self ,request, school, format = None):

		Department = self.get_object(school)

		serialized_Department = DepartmentSerializer(Department, many = True)
		if serialized_Department.data:
			
			Status = status.HTTP_200_OK
		else:
			raise Http404
		return Response({ "Department-Info" : serialized_Department.data, "status" : Status})



class AllDepartmentListApiView(APIView):

	def get_object(self):
		try:
			if not Department.objects.filter(is_active = True):
				raise Http404
			else:
				return Department.objects.filter(is_active = True)

		except Department.DoesNotExist:
			raise Http404
	def get(self ,request , format = None):

		Department = self.get_object()

		serialized_Department = DepartmentSerializer(Department, many = True)

		return Response({ 
							
							"Department-Info" : serialized_Department.data, 
							"status" : status.HTTP_200_OK
						})



class SemesterListApiView(APIView):

	def get_object(self, campus):
		try:
			if not Semester.objects.filter(campus__name = campus):
				raise Http404
			else:
				return Semester.objects.filter(campus__name = campus)

		except Semester.DoesNotExist:
			raise Http404
	def get(self, request, campus, format = None):

		semester = self.get_object(campus)
		serialized_Semester = SemesterSerializer(semester, many = True)

		return Response({ 
						
						"Semester-Info" : serialized_Semester.data, 
						"status" : status.HTTP_200_OK
					})

class SemesterDetailApiView(APIView):

	def get_object(self, semes):
		try:
			if not Semester.objects.get(semes_number = semes):
				raise Http404
			else:
				return Semester.objects.get(semes_number = semes)

		except Semester.DoesNotExist:
			raise Http404
	def get(self ,request , semes, format = None):

		Semester = self.get_object(semes)

		serialized_Semester = SemesterSerializer(Semester)

		return Response({ 
							
							"Semester-Info" : serialized_Semester.data, 
							"status" : status.HTTP_200_OK
						})

class SchoolListApiView(APIView):

	def get_object(self):
		try:
			if not School.objects.filter(is_active = True):
				raise Http404
			else:
				return School.objects.filter(is_active = True)

		except School.DoesNotExist:
			raise Http404
	def get(self ,request , format = None):

		School = self.get_object()

		serialized_School = SchoolSerializer(School, many = True)

		return Response({ 
							
							"School-Info" : serialized_School.data, 
							"status" : status.HTTP_200_OK
						})

class SchoolDetailApiView(APIView):

	def get_object(self, name):
		try:
			if not School.objects.filter(is_active = True).get(name = name):
				raise Http404
			else:
				return School.objects.filter(is_active = True).get(name = name)

		except School.DoesNotExist:
			raise Http404
	def get(self ,request , name, format = None):

		School = self.get_object(name)

		serialized_School = SchoolSerializer(School)

		return Response({ 
							
							"School-Info" : serialized_School.data, 
							"status" : status.HTTP_200_OK
						})





# class CourseMaterialDetailByFormatApiView(APIView):


# 	def get_object(self, course_code):
# 		try:
# 			return CourseMaterial.objects.get(course_code = course_code)
# 		except CourseMaterial.DoesNotExist:
# 			raise Http404
# 	def available_format(self, course_code):
# 		available_formats = []
# 		if LecturePPT.objects.filter(cm__course_code = course_code):
# 			available_formats.append('PPT')

# 		if LecturePDF.objects.filter(cm__course_code = course_code):
# 			available_formats.append('PDF')

# 		if LectureBook.objects.filter(cm__course_code = course_code):
# 			available_formats.append('Book')
# 		return available_formats
	

# 	def get(self ,request , course_code = None, file_format = None, format = None):
	    
# 		course_material = self.get_object(course_code)
# 		available_formats = self.available_format(course_code)
# 		if file_format.lower() == 'ppt':
# 		    course_files = LecturePPT.objects.filter(cm__course_code = course_code)
# 		    serialized_LectureFile = PPTSerializer(course_files , many = True)
# 		elif file_format.lower() == 'pdf':
# 			course_files = LecturePDF.objects.filter(cm__course_code = course_code)
# 			serialized_LectureFile = PDFSerializer(course_files , many = True)
# 		elif file_format.lower() == 'book':
# 		    course_files = LectureBook.objects.filter(cm__course_code = course_code)
# 		    serialized_LectureFile = BookSerializer(course_files , many = True)
# 		else:
# 			return Response({
# 		    "status" : status.HTTP_404_NOT_FOUND,
# 		    "error description" : "Invalid File Format",
# 		    "message" : f'available file formats{available_formats}', 

# 		})


	
# 		##serializing CourseMaterial 
# 		serialized_courseMaterial = CourseMaterialSerializer(course_material)


# 		return Response({
# 			"CourseMaterial-Info" : serialized_courseMaterial.data,
# 			# "CourseMaterial-Files" : serialized_LectureFile.data, 
	  
# 	    })