from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from assignments.models import Assignment
from .models import Submission

@login_required
def student_dashboard(request):
    assignments = Assignment.objects.all()
    submitted = Submission.objects.filter(student= request.user).count()
    total_assignments = assignments.count()
    pending = total_assignments - submitted

    context = {'assignments': assignments,
               'submitted': submitted,
               'pending': pending,
               'total_assignments': total_assignments,
               }
    
    return render(request, 'student_dashboard.html', context)

@login_required
def submitted_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment,id = assignment_id)

    if request.method == 'POST':
        file = request.FILES['file']
        Submission.objects.create(assignment= assignment,student= request.user, file= file)
        
        return redirect('student_dashboard')
    context = {
        'assignment': assignment,
    }
    return render(request, 'submit_assignment.html', context)


@login_required
def view_submissions(request, assignment_id):

    submissions = Submission.objects.all()

    context = {
        'submissions': submissions
    }

    return render(
        request,
        'view_submissions.html',
        context
    )