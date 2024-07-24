from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from company import models as TMODEL
from interviewee import models as SMODEL
from company import forms as TFORM
from interviewee import forms as SFORM
from django.contrib.auth.models import User



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'exam/index.html')


def is_company(user):
    return user.groups.filter(name='COMPANY').exists()

def is_interviewee(user):
    return user.groups.filter(name='INTERVIEWEE').exists()

def afterlogin_view(request):
    if is_interviewee(request.user):
        return redirect('interviewee/interviewee-dashboard')
                
    elif is_company(request.user):
        accountapproval=TMODEL.Company.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('company/company-dashboard')
        else:
            return render(request,'company/company_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_interviewee':SMODEL.Interviewee.objects.all().count(),
    'total_company':TMODEL.Company.objects.all().filter(status=True).count(),
    'total_job':models.Job.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_company_view(request):
    dict={
    'total_company':TMODEL.Company.objects.all().filter(status=True).count(),
    'pending_company':TMODEL.Company.objects.all().filter(status=False).count(),
    'salary':TMODEL.Company.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'exam/admin_company.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_company_view(request):
    companies= TMODEL.Company.objects.all().filter(status=True)
    return render(request,'exam/admin_view_company.html',{'companies':companies})


@login_required(login_url='adminlogin')
def update_company_view(request,pk):
    company=TMODEL.Company.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=company.user_id)
    userForm=TFORM.CompanyUserForm(instance=user)
    companyForm=TFORM.CompanyForm(request.FILES,instance=company)
    mydict={'userForm':userForm,'companyForm':companyForm}
    if request.method=='POST':
        userForm=TFORM.CompanyUserForm(request.POST,instance=user)
        companyForm=TFORM.CompanyForm(request.POST,request.FILES,instance=company)
        if userForm.is_valid() and companyForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            companyForm.save()
            return redirect('admin-view-company')
    return render(request,'exam/update_company.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_company_view(request,pk):
    company=TMODEL.Company.objects.get(id=pk)
    user=User.objects.get(id=company.user_id)
    user.delete()
    company.delete()
    return HttpResponseRedirect('/admin-view-company')




@login_required(login_url='adminlogin')
def admin_view_pending_company_view(request):
    companies= TMODEL.Company.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_company.html',{'companies':companies})


@login_required(login_url='adminlogin')
def approve_company_view(request,pk):
    companySalary=forms.CompanySalaryForm()
    if request.method=='POST':
        companySalary=forms.CompanySalaryForm(request.POST)
        if companySalary.is_valid():
            company=TMODEL.Company.objects.get(id=pk)
            company.salary=companySalary.cleaned_data['salary']
            company.status=True
            company.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-company')
    return render(request,'exam/salary_form.html',{'companySalary':companySalary})

@login_required(login_url='adminlogin')
def reject_company_view(request,pk):
    company=TMODEL.Company.objects.get(id=pk)
    user=User.objects.get(id=company.user_id)
    user.delete()
    company.delete()
    return HttpResponseRedirect('/admin-view-pending-company')

@login_required(login_url='adminlogin')
def admin_view_company_salary_view(request):
    companies= TMODEL.Company.objects.all().filter(status=True)
    return render(request,'exam/admin_view_company_salary.html',{'companies':companies})




@login_required(login_url='adminlogin')
def admin_interviewee_view(request):
    dict={
    'total_interviewee':SMODEL.Interviewee.objects.all().count(),
    }
    return render(request,'exam/admin_interviewee.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_interviewee_view(request):
    interviewees= SMODEL.Interviewee.objects.all()
    return render(request,'exam/admin_view_interviewee.html',{'interviewees':interviewees})



@login_required(login_url='adminlogin')
def update_interviewee_view(request,pk):
    interviewee=SMODEL.Interviewee.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=interviewee.user_id)
    userForm=SFORM.IntervieweeUserForm(instance=user)
    intervieweeForm=SFORM.IntervieweeForm(request.FILES,instance=interviewee)
    mydict={'userForm':userForm,'intervieweeForm':intervieweeForm}
    if request.method=='POST':
        userForm=SFORM.IntervieweeUserForm(request.POST,instance=user)
        intervieweeForm=SFORM.IntervieweeForm(request.POST,request.FILES,instance=interviewee)
        if userForm.is_valid() and intervieweeForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            intervieweeForm.save()
            return redirect('admin-view-interviewee')
    return render(request,'exam/update_interviewee.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_interviewee_view(request,pk):
    interviewee=SMODEL.Interviewee.objects.get(id=pk)
    user=User.objects.get(id=interviewee.user_id)
    user.delete()
    interviewee.delete()
    return HttpResponseRedirect('/admin-view-interviewee')


@login_required(login_url='adminlogin')
def admin_job_view(request):
    return render(request,'exam/admin_job.html')


@login_required(login_url='adminlogin')
def admin_add_job_view(request):
    jobForm=forms.JobForm()
    if request.method=='POST':
        jobForm=forms.JobForm(request.POST)
        if  jobForm.is_valid():
            jobForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'jobForm':jobForm})


@login_required(login_url='adminlogin')
def admin_view_job_view(request):
    jobs = models.Job.objects.all()
    return render(request,'exam/admin_view_job.html',{'jobs':jobs})

@login_required(login_url='adminlogin')
def delete_job_view(request,pk):
    job=models.Job.objects.get(id=pk)
    job.delete()
    return HttpResponseRedirect('/admin-view-course')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            job=models.Job.objects.get(id=request.POST.get('jobID'))
            question.job=job
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'exam/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    jobs= models.Job.objects.all()
    return render(request,'exam/admin_view_question.html',{'jobs':jobs})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(job_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_interviewee_marks_view(request):
    interviewees= SMODEL.Interviewee.objects.all()
    return render(request,'exam/admin_view_interviewee_marks.html',{'interviewees':interviewees})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    jobs = models.Job.objects.all()
    response = render(request,'exam/admin_view_marks.html',{'jobs':jobs})
    response.set_cookie('interviewee_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    job = models.Job.objects.get(id=pk)
    interviewee_id = request.COOKIES.get('interviewee_id')
    interviewee= SMODEL.Interviewee.objects.get(id=interviewee_id)

    results= models.Result.objects.all().filter(exam=job).filter(interviewee=interviewee)
    return render(request,'exam/admin_check_marks.html',{'results':results})
    




def aboutus_view(request):
    return render(request,'exam/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})


