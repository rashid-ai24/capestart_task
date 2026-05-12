from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assignment
from submissions.models import Submission

@login_required
def teacher_dashboard(request):
    context = {
        'assignments': Assignment.objects.all(),
        'total_assignments': Assignment.objects.count(),
        'total_submissions': Submission.objects.count(),
    }
    return render(request, 'teacher_dashboard.html', context)

@login_required
def create_assignment(request):

    if request.method == 'POST':

        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']

        Assignment.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            teacher=request.user
        )

        return redirect('teacher_dashboard')

    return render(
        request,
        'create_assignment.html'
    )


@login_required
def delete_assignment(request, assignment_id):

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id
    )

    assignment.delete()

    return redirect('teacher_dashboard')
