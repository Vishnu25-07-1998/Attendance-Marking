from django.urls import path
from .import views

urlpatterns = [
    path('add_employee/', views.add_employee, name='add_employee'),
    path('get_all_employees/', views.get_all_employees, name='get_all_employees'),
    path('', views.home),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance_details/', views.get_attendance_details, name='attendance_details'),
    path('employee_details/<int:employee_id>/', views.employee_details, name='employee_details'),
]
