from django.db import models
from datetime import datetime
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class TGUser(models.Model):
	user_tg_id = models.CharField(max_length = 100, unique = True)
	username = models.CharField(max_length = 100, null = True, blank = True)
	first_name = models.CharField(max_length = 100, null = True, blank = True)
	last_name = models.CharField(max_length = 100, null = True, blank = True)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.username + ' : ' + self.first_name if self.username else self.filename
class Campus(models.Model):
	name = models.CharField(max_length = 369)
	about = models.TextField()
	location = models.CharField(max_length = 33)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	is_active = models.BooleanField(default = True)


	def __str__(self):
		return self.name


class School(models.Model):
	department = models.ManyToManyField(to = 'Department', related_name = 'school')
	name = models.CharField(max_length = 369)
	about = models.TextField()
	is_active = models.BooleanField(default = True)

	def __str__(self):
		return self.name



class Department(models.Model):
	name = models.CharField(max_length = 600)
	short_name = models.CharField(max_length = 369)
	is_active = models.BooleanField(default = True)


	def __str__(self):
		return self.short_name

class Semester(models.Model):
	name = models.CharField(max_length = 369)
	semes_number = models.IntegerField()
	school_in_this_semes = models.ManyToManyField(to = School)
	campus = models.ForeignKey(to = Campus, related_name = 'semester', on_delete = models.SET_NULL, null = True)

	def __str__(self):
		return self.name




class CourseMaterial(models.Model):
	SEMESTERCHOICE = (('1', 'Freshman 1st'),('2', 'Freshman 2nd'),('3', 'Sophomore 1st'),('4', 'Sophomore 2nd'),('5', 'Junior 1st'),('6', 'Junior 2nd'),('7', 'Senior 1st'),('8', 'Senior 2nd'),('9', 'GC 1st'),('10', 'GC 2nd'),)
	def upload_to_thumb_dir(self, filename):
		dt = str(datetime.now().date()) + str( datetime.now().time())
		path = f'{self.course_name}_{self.course_code}/{self.created_by}/{dt}/{filename}'
		return path

	course_code = models.CharField(max_length = 369)
	course_name = models.CharField(max_length = 369)
	course_description = models.TextField(help_text = "About the course / files atched to this course")
	thumbnail = models.ImageField(upload_to = upload_to_thumb_dir, blank = True, null = True)
	semester = models.ForeignKey(to = Semester, on_delete = models.SET_NULL, null = True)
	# semester = models.CharField(max_length = 2, choices = SEMESTERCHOICE)
	department = models.ForeignKey(to = Department, on_delete = models.CASCADE, related_name = "course_materials")
	created_by = models.CharField(max_length = 369, default = 'MrPGuy', blank = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	is_active = models.BooleanField(default = True)


	def __str__(self):
		return f'{self.course_name} : {self.course_code}'


class AssignmentExam(models.Model):
	
	def upload_to_thumb_dir(self, filename):
		dt = str(datetime.now().date()) + str(datetime.now().time())
		if self.created_by:
			path = f'{self.course_name}_{self.course_code}/{self.created_by}/{dt}/{filename}'
		else:
			path = f'{self.course_name}_{self.course_code}/{self.semester}/{dt}/{filename}'
		return path
	
	course_code = models.CharField(max_length = 369)
	course_name = models.CharField(max_length = 369)
	semester = models.CharField(max_length = 369)
	additional_info = models.TextField(null = True, blank = True)
	created_by = models.CharField(max_length = 369, null = True, blank = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	is_active = models.BooleanField(default = True)



	def __str__(self):
		return f'{self.course_name} : {self.course_code}'



class LectureBook(models.Model):
	
	def upload_to_books_dir(self, filename):
		dt = str(datetime.now().date()) + str( datetime.now().time())
		path = f'{self.cm.department.name}/{self.cm.semester.name}/{self.cm.course_name}_{self.cm.course_code}/BOOK/{self.title}/{dt}/{filename}'
		return path
	
	cm = models.ForeignKey(to = CourseMaterial, related_name = 'books', on_delete = models.CASCADE)
	book = models.FileField(upload_to = upload_to_books_dir, null = True, blank = True, storage=RawMediaCloudinaryStorage())
	tg_file_id = models.CharField(max_length = 255)
	tg_file_url = models.CharField(max_length = 255, null = True, blank = True)
	title = models.CharField(max_length = 369, help_text = 'chapter or specific title related to this file ', null = True, blank = True)

	def __str__(self):
		return self.title + ':' + self.cm.course_name if self.title else self.cm.course_name


class LecturePPT(models.Model):
	
	def upload_to_ppt_dir(self, filename):
		dt = str(datetime.now().date()) + str(datetime.now().time())
		path = f'{self.cm.department.name}/{self.cm.semester.name}/{self.cm.course_name}_{self.cm.course_code}/PPT/{self.title}/{dt}/{filename}'
		return path
	
	cm = models.ForeignKey(to = CourseMaterial, related_name = 'ppts', on_delete = models.CASCADE)
	ppt = models.FileField(upload_to = upload_to_ppt_dir, null = True, blank = True, storage=RawMediaCloudinaryStorage())
	tg_file_id = models.CharField(max_length = 255)
	tg_file_url = models.CharField(max_length = 255, null = True, blank = True)
	title = models.CharField(max_length = 369, help_text = 'chapter or specific title related to this file ', null = True, blank = True)

	def __str__(self):
		return self.title + ':' + self.cm.course_name if self.title else self.cm.course_name


class LecturePDF(models.Model):
	
	def upload_to_pdf_dir(self, filename):
		dt = str(datetime.now().date()) + str( datetime.now().time())
		path = f'{self.cm.department.name}/{self.cm.semester.name}/{self.cm.course_name}_{self.cm.course_code}/PDF/{self.title}/{dt}/{filename}'
		return path
	
	cm = models.ForeignKey(to = CourseMaterial, related_name = 'pdfs', on_delete = models.CASCADE)
	pdf = models.FileField(upload_to = upload_to_pdf_dir, null = True, blank = True, storage=RawMediaCloudinaryStorage())
	tg_file_id = models.CharField(max_length = 255)
	tg_file_url = models.CharField(max_length = 255, null = True, blank = True)
	title = models.CharField(max_length = 369, help_text = 'chapter or specific title related to this file ', null = True, blank = True)

	def __str__(self):
		return self.title + ':' + self.cm.course_name if self.title else self.cm.course_name


class Image(models.Model):
	
	def upload_to_img_dir(self, filename):
		dt = str(datetime.now().date()) + str( datetime.now().time())
		path = f'{self.cm.department.name}/{self.cm.semester.name}/{self.cm.course_name}_{self.cm.course_code}/IMAGE/{self.title}/{dt}/{filename}'
		return path
	
	cm = models.ForeignKey(to = AssignmentExam, related_name = 'images', on_delete = models.CASCADE)
	img = models.ImageField(upload_to = upload_to_img_dir, null = True, blank = True)
	tg_file_id = models.CharField(max_length = 255)
	tg_file_url = models.CharField(max_length = 255, null = True, blank = True)
	title = models.CharField(max_length = 369, help_text = 'chapter or specific title related to this file ', null = True, blank = True)

	def __str__(self):
		return self.title + ':' + self.cm.course_name if self.title else self.cm.course_name
