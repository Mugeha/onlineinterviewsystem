from django.urls import path, include
from django.contrib import admin
from exam import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('company/', include('company.urls')),
    path('interviewee/', include('interviewee.urls')),

    path('', views.home_view, name=''),
    path('logout', LogoutView.as_view(template_name='exam/logout.html'), name='logout'),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='exam/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-company', views.admin_company_view, name='admin-company'),
    path('admin-view-company', views.admin_view_company_view, name='admin-view-company'),
    path('update-company/<int:pk>', views.update_company_view, name='update-company'),
    path('delete-company/<int:pk>', views.delete_company_view, name='delete-company'),
    path('admin-view-pending-company', views.admin_view_pending_company_view, name='admin-view-pending-company'),
    path('admin-view-company-salary', views.admin_view_company_salary_view, name='admin-view-company-salary'),
    path('approve-company/<int:pk>', views.approve_company_view, name='approve-company'),
    path('reject-company/<int:pk>', views.reject_company_view, name='reject-company'),

    path('admin-interviewee', views.admin_interviewee_view, name='admin-interviewee'),
    path('admin-view-interviewee', views.admin_view_interviewee_view, name='admin-view-interviewee'),
    path('admin-view-interviewee-marks', views.admin_view_interviewee_marks_view, name='admin-view-interviewee-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view, name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view, name='admin-check-marks'),
    path('update-interviewee/<int:pk>', views.update_interviewee_view, name='update-interviewee'),
    path('delete-interviewee/<int:pk>', views.delete_interviewee_view, name='delete-interviewee'),

    path('admin-job', views.admin_job_view, name='admin-job'),
    path('admin-add-job', views.admin_add_job_view, name='admin-add-job'),
    path('admin-view-job', views.admin_view_job_view, name='admin-view-job'),
    path('delete-job/<int:pk>', views.delete_job_view, name='delete-job'),

    path('admin-question', views.admin_question_view, name='admin-question'),
    path('admin-add-question', views.admin_add_question_view, name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view, name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view, name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view, name='delete-question'),

]
