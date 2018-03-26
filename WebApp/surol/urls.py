from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('signup/',views.signup,name='signup'),
	path('home/',views.index, name='home'),
	path('student/',views.studenthome, name='studenthome'),
	path('student/<int:student_id>/remove_deadline/<int:deadline_id>',views.removeDeadlineStudent,name='remove_pdeadline'),
	path('professor/',views.professorhome, name='professorhome'),
	path('course/<int:course_id>/', views.course, name='course_page'),
	path('course/<int:course_id>/register_student',views.registerStudent,name='register_student'),
	path('course/<int:course_id>/deregister_student/<int:student_id>',views.deregisterStudent,name='deregister_student'),
	path('course/<int:course_id>/add_deadline',views.addDeadline,name='add_deadline'),
	path('course/<int:course_id>/remove_deadline/<int:deadline_id>',views.removeDeadline,name='remove_deadline'),
]
