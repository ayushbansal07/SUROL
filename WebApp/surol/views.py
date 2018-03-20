from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User

# Create your views here.
def studenthome(request):
	#id = int(request.POST['id'])
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/surol/home")

	id = int(request.user.username[1:])
	print(id)

	if request.method == 'POST':
		date = request.POST['date']
		name = request.POST['name']
		comments = request.POST['comments']

		deadline = Personal_deadline(student=Student.objects.filter(pk=id)[0],name=name,date=date,comments=comments)
		deadline.save()


	student_info = Student.objects.filter(pk=id)
	registers = Registers.objects.filter(student=id)
	result = []
	p_deadlines = Personal_deadline.objects.filter(student=id)

	for deadline in p_deadlines:
		result.append((deadline.date,deadline.name,deadline.comments))

	for register in registers:
		c_deadlines = Course_deadline.objects.filter(course=register.course)
		for deadline in c_deadlines:
			result.append((deadline.date,deadline.name,deadline.comments))

	result.sort(key = lambda x : x[0])
	context = {'id':id,
		'Student_info': student_info[0],
		'Registers' : registers,
		'Deadlines' : result
	}

	return render(request,'surol/student.html', context)


def professorhome(request):
	#id = int(request.POST['id'])
	id = int(request.user.username[1:])
	takes = Takes.objects.filter(professor=id)
	context = {
		'id' : id,
		'Takes' : takes
	}
	return render(request,'surol/professor.html',context)


def index(request):
	if request.user.is_authenticated:
		username = request.user.username
		#password = request.user.password
		#return render(request,'surol/index.html',{'username' : username})
		if(username[0] == 'S'):
			return HttpResponseRedirect("/surol/student/")
		elif(username[0] == 'P'):
			return HttpResponseRedirect("/surol/professor/")

	else:
		return HttpResponseRedirect("/surol/home")




def signup(request):
	if request.method == 'POST':
		user_type = int(request.POST['user_type'])
		name = request.POST['name']
		email = request.POST['email']
		dept_name = request.POST['dept_name']
		password = request.POST['password']
		try:
			if(user_type == 0):
				s = Student(name=name,email=email,dept_name=dept_name,password=password)
				s.save()
				user = User.objects.create_user(username='S'+str(s.id),email=email, password=password)
				user.save()
				return render(request,'surol/display_id.html',{'user_id' : 'S'+str(s.id)})
			else:
				p = Professor(name=name,email=email,dept_name=dept_name,password=password)
				p.save()
				user = User.objects.create_user(username='P'+str(p.id),email=email, password=password)
				user.save()
				return render(request,'surol/display_id.html',{'user_id' : 'P'+str(p.id)})
		except:
			print("Error In Signup")
	else:
		return render(request,'surol/signup.html')

def homepage(request):
	return render(request,'surol/home.html')

def check_prof(request,course_id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect("/surol/home")

	user_id = request.user.username
	if user_id[0] != 'P':
		return HttpResponseRedirect("/surol/student")
	id = int(user_id[1:])
	takes_obj = Takes.objects.filter(professor=id,course=course_id)
	if len(takes_obj) != 1:
		return HttpResponseRedirect("/surol/professor")	

def get_course_data(request,course_id):
	course_deadlines = Course_deadline.objects.filter(course=course_id).order_by('date')
	registered= Registers.objects.filter(course=course_id)
	enrolled_students = []
	for entry in registered:
		enrolled_students.append(Student.objects.filter(pk=entry.student.id)[0])

	#print(enrolled_students)

	other_deadlines = {}

	for student in enrolled_students :
		student_courses = Registers.objects.filter(student=student.id)
		student_courses_deadlines = []
		for entry in student_courses:
			if entry.course.id != course_id:
				student_courses_deadlines.extend(Course_deadline.objects.filter(course = entry.course.id))
		for entry in student_courses_deadlines:
			if entry not in other_deadlines:
				other_deadlines[entry] = 0
			other_deadlines[entry] += 1

	other_deadlines = sorted(other_deadlines.items(),key=lambda x : x[0].date)
	return course_deadlines, enrolled_students, other_deadlines	

def course(request,course_id):
	#user_id =request.user.username[1:]
	response = check_prof(request,course_id)
	if isinstance(response,HttpResponseRedirect):
		return response

	course_deadlines, enrolled_students, other_deadlines = get_course_data(request,course_id)

	return render(request, 'surol/course.html',{'id' : request.user.username,
		'course_id' : course_id,
		'Course_deadlines' : course_deadlines,
		'Enrolled_students' : enrolled_students,
		'Other_deadlines' : other_deadlines})

def registerStudent(request, course_id):
	response = check_prof(request,course_id)
	if isinstance(response,HttpResponseRedirect):
		return response

	if request.method == 'POST':
		try:
			student_id = int(request.POST['student_id'])
		except:
			course_deadlines, enrolled_students, other_deadlines = get_course_data(request,course_id)
			return render(request,'surol/course.html',{
				'id' : request.user.username,
				'course_id' : course_id,
				'error_msg' : "Student Id must be an integer!!",
				'Course_deadlines' : course_deadlines,
				'Enrolled_students' : enrolled_students,
				'Other_deadlines' : other_deadlines
			})
		r_prev = Registers.objects.filter(student=student_id,course=course_id)
		if len(r_prev) != 0:
			print("User Already exists")
			course_deadlines, enrolled_students, other_deadlines = get_course_data(request,course_id)
			return render(request,'surol/course.html',{
				'id' : request.user.username,
				'course_id' : course_id,
				'error_msg' : "Student Already Registered!!",
				'Course_deadlines' : course_deadlines,
				'Enrolled_students' : enrolled_students,
				'Other_deadlines' : other_deadlines
			})
		try:
			r = Registers(student=Student.objects.filter(pk=student_id)[0],course=Course.objects.filter(pk=course_id)[0])
			r.save()
		except:
			course_deadlines, enrolled_students, other_deadlines = get_course_data(request,course_id)
			return render(request,'surol/course.html',{
				'id' : request.user.username,
				'course_id' : course_id,
				'error_msg' : "Student Does not Exist!!",
				'Course_deadlines' : course_deadlines,
				'Enrolled_students' : enrolled_students,
				'Other_deadlines' : other_deadlines
			})
		return HttpResponseRedirect("/surol/course/"+str(course_id))
	else:
		course_deadlines, enrolled_students, other_deadlines = get_course_data(request,course_id)
		return render(request,'surol/course.html',{
				'id' : request.user.username,
				'course_id' : course_id,
				'error_msg' : "Invalid Access!!",
				'Course_deadlines' : course_deadlines,
				'Enrolled_students' : enrolled_students,
				'Other_deadlines' : other_deadlines
			})

def deregisterStudent(request,course_id,student_id):
	response = check_prof(request,course_id)
	if isinstance(response,HttpResponseRedirect):
		return response

	try:
		r = Registers.objects.filter(student=student_id,course=course_id).delete()
	except Exception as e:
		print("Error : ",e)
		course_deadlines, enrolled_students, other_deadlines = get_course_data(request,course_id)
		return render(request,'surol/course.html',{
			'id' : request.user.username,
			'course_id' : course_id,
			'error_msg' : "Student Not Registered!!",
			'Course_deadlines' : course_deadlines,
			'Enrolled_students' : enrolled_students,
			'Other_deadlines' : other_deadlines
		})

	return HttpResponseRedirect("/surol/course/"+str(course_id))

def addDeadline(request,course_id):
	response = check_prof(request,course_id)
	if isinstance(response,HttpResponseRedirect):
		return response

	if request.method =='POST':
		date = request.POST['date']
		name = request.POST['name']
		comments = request.POST['comments']

		deadline = Course_deadline(course=Course.objects.filter(pk=course_id)[0],name=name,date=date,comments=comments)
		deadline.save()

		return HttpResponseRedirect("/surol/course/"+str(course_id))
	else:
		course_deadlines, enrolled_students, other_deadlines = get_course_data(request,course_id)
		return render(request,'surol/course.html',{
				'id' : request.user.username,
				'course_id' : course_id,
				'error_msg' : "Invalid Access!!",
				'Course_deadlines' : course_deadlines,
				'Enrolled_students' : enrolled_students,
				'Other_deadlines' : other_deadlines
			})


def removeDeadline(request,course_id,deadline_id):
	response = check_prof(request,course_id)
	if isinstance(response,HttpResponseRedirect):
		return response

	try:
		d = Course_deadline.objects.filter(pk=deadline_id).delete()
	except Exception as e:
		print("Error : ",e)
		course_deadlines, enrolled_students, other_deadlines = get_course_data(request,course_id)
		return render(request,'surol/course.html',{
			'id' : request.user.username,
			'course_id' : course_id,
			'error_msg' : "Deadline not Removed!!",
			'Course_deadlines' : course_deadlines,
			'Enrolled_students' : enrolled_students,
			'Other_deadlines' : other_deadlines
		})
	return HttpResponseRedirect("/surol/course/"+str(course_id))