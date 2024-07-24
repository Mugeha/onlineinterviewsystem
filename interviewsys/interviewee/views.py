from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from company import models as TMODEL


#for showing signup/login button for interviewee
def intervieweeclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'interviewee/intervieweeclick.html')

def interviewee_signup_view(request):
    userForm=forms.IntervieweeUserForm()
    intervieweeForm=forms.IntervieweeForm()
    mydict={'userForm':userForm,'intervieweeForm':intervieweeForm}
    if request.method=='POST':
        userForm=forms.IntervieweeUserForm(request.POST)
        intervieweeForm=forms.IntervieweeForm(request.POST,request.FILES)
        if userForm.is_valid() and intervieweeForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            interviewee=intervieweeForm.save(commit=False)
            interviewee.user=user
            interviewee.save()
            my_interviewee_group = Group.objects.get_or_create(name='INTERVIEWEE')
            my_interviewee_group[0].user_set.add(user)
        return HttpResponseRedirect('intervieweelogin')
    return render(request,'interviewee/intervieweesignup.html',context=mydict)

def is_interviewee(user):
    return user.groups.filter(name='INTERVIEWEE').exists()

@login_required(login_url='intervieweelogin')
@user_passes_test(is_interviewee)
def interviewee_dashboard_view(request):
    dict={
    
    'total_job':QMODEL.Job.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'interviewee/interviewee_dashboard.html',context=dict)

@login_required(login_url='intervieweelogin')
@user_passes_test(is_interviewee)
def interviewee_exam_view(request):
    jobs=QMODEL.Job.objects.all()
    return render(request,'interviewee/interviewee_exam.html',{'jobs':jobs})

@login_required(login_url='intervieweelogin')
@user_passes_test(is_interviewee)
def take_exam_view(request,pk):
    job=QMODEL.Job.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(job=job).count()
    questions=QMODEL.Question.objects.all().filter(job=job)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'interviewee/take_exam.html',{'job':job,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='intervieweelogin')
@user_passes_test(is_interviewee)
def start_exam_view(request,pk):
    job=QMODEL.Job.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(job=job)
    if request.method=='POST':
        pass
    response= render(request,'interviewee/start_exam.html',{'job':job,'questions':questions})
    response.set_cookie('company_id',job.id)
    return response


@login_required(login_url='intervieweelogin')
@user_passes_test(is_interviewee)
def calculate_marks_view(request):
    if request.COOKIES.get('job_id') is not None:
        job_id = request.COOKIES.get('job_id')
        job = QMODEL.Job.objects.get(id=job_id)

        total_marks = 0
        questions = QMODEL.Question.objects.filter(job=job)

        for i, question in enumerate(questions, start=1):
            selected_ans = request.COOKIES.get(str(i))
            actual_answer = question.answer
            if selected_ans == actual_answer:
                total_marks += question.marks

        interviewee = models.Interviewee.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total_marks
        result.exam = job
        result.interviewee = interviewee
        result.save()

        return HttpResponseRedirect(reverse('view-result'))

    # If job_id is None, redirect to some other view or handle accordingly
    # For example, redirect to homepage
    return HttpResponseRedirect(reverse('interviewee-dashboard'))

@login_required(login_url='intervieweelogin')
@user_passes_test(is_interviewee)
def view_result_view(request):
    jobs=QMODEL.Job.objects.all()
    return render(request,'interviewee/view_result.html',{'jobs':jobs})
    

@login_required(login_url='intervieweelogin')
@user_passes_test(is_interviewee)
def check_marks_view(request,pk):
    job=QMODEL.Job.objects.get(id=pk)
    interviewee = models.Interviewee.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=job).filter(interviewee=interviewee)
    return render(request,'interviewee/check_marks.html',{'results':results})

@login_required(login_url='intervieweelogin')
@user_passes_test(is_interviewee)
def student_marks_view(request):
    jobs=QMODEL.Job.objects.all()
    return render(request,'interviewee/interviewee_marks.html',{'jobs':jobs})
  