from .models import *
from rest_framework import serializers

class TGUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = TGUser
		fields = '__all__'

class PPTSerializer(serializers.ModelSerializer):
	class Meta:
		model = LecturePPT
		fields = '__all__'
		
class PDFSerializer(serializers.ModelSerializer):
	class Meta:
		model = LecturePDF
		fields = '__all__'
class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = LectureBook
		fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
	department = DepartmentSerializer(many=True, read_only=True)
	class Meta:
		model = School
		fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
	school_in_this_semes = SchoolSerializer(many=True, read_only=True)
	class Meta:
		model = Semester
		fields = '__all__'




class CourseMaterialSerializer(serializers.ModelSerializer):
	ppts = PPTSerializer(many = True, read_only = True)
	pdfs = PDFSerializer(many = True, read_only = True)
	books = BookSerializer(many = True, read_only = True)
	department = DepartmentSerializer(read_only = True)
	class Meta:
		model = CourseMaterial
		# fields = '__all__'
		read_only_fields = (

			'course_code',
			'course_name',
			'course_description',
			'thumbnail',
			'semester',
			'department',
			'created_by',
			'created_at',
			'updated',
			'ppts',
			'pdfs',
			'books',


			)
		exclude = ('is_active',)