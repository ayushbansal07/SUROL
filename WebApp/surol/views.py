from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Student, Professor
# Create your views here.
def index(request):
	return HttpResponse("Hello")

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
			else:
				p = Professor(name=name,email=email,dept_name=dept_name,password=password)
				p.save()
			return HttpResponseRedirect("/surol")
		except:
			print("NHP################")
	else:
		return render(request,'surol/signup.html')

	