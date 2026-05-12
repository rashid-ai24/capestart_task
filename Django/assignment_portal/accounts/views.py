from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.profile.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



from django.http import HttpResponse

def teacher_dashboard(request):
    return HttpResponse("Teacher Dashboard")

def student_dashboard(request):
    return HttpResponse("Student Dashboard")