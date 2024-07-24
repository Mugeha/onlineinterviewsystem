from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from interviewee import models as SMODEL
from exam import forms as QFORM


#for showing signup/login button for company
def companyclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'company/companyclick.html')

def company_signup_view(request):
    userForm=forms.CompanyUserForm()
    companyForm=forms.CompanyForm()
    mydict={'userForm':userForm,'companyForm':companyForm}
    if request.method=='POST':
        userForm=forms.CompanyUserForm(request.POST)
        companyForm=forms.CompanyForm(request.POST,request.FILES)
        if userForm.is_valid() and companyForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            company=companyForm.save(commit=False)
            company.user=user
            company.save()
            my_company_group = Group.objects.get_or_create(name='COMPANY')
            my_company_group[0].user_set.add(user)
        return HttpResponseRedirect('companylogin')
    return render(request,'company/companysignup.html',context=mydict)



def is_company(user):
    return user.groups.filter(name='COMPANY').exists()

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_dashboard_view(request):
    dict={
    
    'total_job':QMODEL.Job.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_interviewee':SMODEL.Interviewee.objects.all().count()
    }
    return render(request,'company/company_dashboard.html',context=dict)

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_exam_view(request):
    return render(request,'company/company_exam.html')


@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_add_exam_view(request):
    jobForm=QFORM.JobForm()
    if request.method=='POST':
        jobForm=QFORM.JobForm(request.POST)
        if jobForm.is_valid():
            jobForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/company/company-view-exam')
    return render(request,'company/company_add_exam.html',{'jobForm':jobForm})

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_view_exam_view(request):
    jobs = QMODEL.Job.objects.all()
    return render(request,'company/company_view_exam.html',{'jobs':jobs})

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def delete_exam_view(request,pk):
    job=QMODEL.Job.objects.get(id=pk)
    job.delete()
    return HttpResponseRedirect('/company/company-view-exam')

@login_required(login_url='adminlogin')
def company_question_view(request):
    return render(request,'company/company_question.html')

@login_required(login_url='companylogin')
@user_passes_test(is_company )
def company_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            job=QMODEL.Job.objects.get(id=request.POST.get('jobID'))
            question.job=job
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/company/company-view-question')
    return render(request,'company/company_add_question.html',{'questionForm':questionForm})

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def company_view_question_view(request):
    jobs= QMODEL.Job.objects.all()
    return render(request,'company/company_view_question.html',{'jobs':jobs})

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(job_id=pk)
    return render(request,'company/see_question.html',{'questions':questions})

@login_required(login_url='companylogin')
@user_passes_test(is_company)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/company/company-view-question')
