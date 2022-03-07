from django.urls import path , re_path, include
from .views import *



urlpatterns = [

    path('cms' , CourseMaterialListApiView.as_view(), name = "cm_list"),
    path('cms/<str:course_code>' , CourseMaterialFastApiView.as_view() , name = "fast_cm"),
    path('cms/<int:semester>/<int:department>' , CourseMaterialListBySemesterDepartmentApiView.as_view() , name = "cm_by_semester_department"),
    path('cms/department/<str:department>' , CourseMaterialListByDepartmentApiView.as_view() , name = "cm_by_department"),
    path('cms/<int:semester>/<int:department>/<str:course_code>' , CourseMaterialDetailApiView.as_view() , name = "cm_detail"),
    path('schools' , SchoolListApiView.as_view(), name = "school_list"),
    path('schools/<str:name>' , SchoolDetailApiView.as_view(), name = "school_detail"),
    path('<str:campus>/semesters' , SemesterListApiView.as_view(), name = "semester_list"),
    path('semesters/<int:semes>' , SemesterDetailApiView.as_view(), name = "semester_detail"),
    path('departments' , AllDepartmentListApiView.as_view(), name = "department_list"),
    path('department/<str:school>' , DepartmentListApiView.as_view(), name = "department_list"),
    path('tguser' , TGUserCreateApiView.as_view(), name = "tg_user_create"),
    path('ppt' , LecturePPTCreateApiView.as_view(), name = "ppt_create"),
    path('pdf' , LecturePDFCreateApiView.as_view(), name = "pdf_create"),
    path('book' , LectureBookCreateApiView.as_view(), name = "book_create"),

]