from django.contrib import admin
from .models import *


class LecturePPTInline(admin.TabularInline):
	model = LecturePPT
	raw_id_fields = ['cm']
class LecturePDFInline(admin.TabularInline):
	model = LecturePDF
	raw_id_fields = ['cm']
class LectureBookInline(admin.TabularInline):
	model = LectureBook
	raw_id_fields = ['cm']

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
	list_display = ['course_name', 'course_code', 'semester', 'created_by', 'updated', 'is_active']
	list_filter = ['course_name', 'created_by', 'updated']
	inlines = [LecturePPTInline, LecturePDFInline, LectureBookInline]



@admin.register(AssignmentExam)
class AssignmentExamAdmin(admin.ModelAdmin):
	list_display = ['course_name', 'course_code', 'semester', 'created_by', 'updated', 'is_active']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ['short_name', 'name']

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
	list_display = ['name']

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
	list_display = ['name', 'updated']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
	list_display = ['name']
@admin.register(TGUser)
class TGUserAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'username', 'updated']


@admin.register(LecturePPT)
class LecturePPTAdmin(admin.ModelAdmin):
	list_display = ['cm', 'tg_file_id']
@admin.register(LecturePDF)
class LecturePDFAdmin(admin.ModelAdmin):
	list_display = ['cm', 'tg_file_id']
@admin.register(LectureBook)
class LectureBookAdmin(admin.ModelAdmin):
	list_display = ['cm', 'tg_file_id']