from django.urls import path
from interviewee import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('intervieweeclick', views.intervieweeclick_view),
path('intervieweelogin', LoginView.as_view(template_name='interviewee/intervieweelogin.html'),name='intervieweelogin'),
path('intervieweesignup', views.interviewee_signup_view,name='intervieweesignup'),
path('interviewee-dashboard', views.interviewee_dashboard_view,name='interviewee-dashboard'),
path('interviewee-exam', views.interviewee_exam_view,name='interviewee-exam'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('start-exam/<int:pk>', views.start_exam_view,name='start-exam'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('interviewee-marks', views.student_marks_view,name='interviewee-marks'),
]