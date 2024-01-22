from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import EmployeeDetail, Employee
from .serializers import EmployeeSerializer, EmployeeDetailSerializer
from datetime import datetime, timedelta



# Create your views here.
def home(request):
    employees = EmployeeDetail.objects.all()
    return render(request,'home.html', {'employees' : employees})



@api_view(['POST'])
def add_employee(request):
    if request.method == 'POST':
        serializer = EmployeeDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def get_all_employees(request):
    if request.method == 'GET':
        employees = EmployeeDetail.objects.all()
        serializer = EmployeeDetailSerializer(employees, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def mark_attendance(request):
    if request.method == 'POST':
        employee_id = request.data.get('employee')
        date = request.data.get('date')
        is_present = request.data.get('is_present', False)
        check_in_time_str = request.data.get('check_in_time', None)
        check_out_time_str = request.data.get('check_out_time', None)

        try:
            employee = EmployeeDetail.objects.get(pk=employee_id)
        except EmployeeDetail.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            if is_present:
                if check_in_time_str:
                    check_in_time = datetime.strptime(check_in_time_str, '%Y-%m-%dT%H:%M:%S')
                    serializer.validated_data['check_in_time'] = check_in_time

                if check_out_time_str:
                    check_out_time = datetime.strptime(check_out_time_str, '%Y-%m-%dT%H:%M:%S')
                    serializer.validated_data['check_out_time'] = check_out_time

                    # Calculate work duration
                    work_duration = check_out_time - check_in_time
                    serializer.validated_data['work_duration'] = work_duration

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_attendance_details(request):
    employee_id = request.GET.get('employee_id')

    try:
        employee = EmployeeDetail.objects.get(pk=employee_id)
    except EmployeeDetail.DoesNotExist:
        return Response({'error': f'Employee with ID {employee_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    attendance_details = Employee.objects.filter(employee=employee)
    serializer = EmployeeSerializer(attendance_details, many=True)
    return Response(serializer.data)


def employee_details(request, employee_id):
    try:
        employee = EmployeeDetail.objects.get(pk=employee_id)
    except EmployeeDetail.DoesNotExist:
        # Handle the case where the employee does not exist
        return render(request, 'employee_details.html', {'error': 'Employee not found'})

    attendance_details = Employee.objects.filter(employee=employee)
    serializer = EmployeeSerializer(attendance_details, many=True)
    context = {
        'employee': employee,
        'attendance_details': serializer.data,
    }
    return render(request, 'employee_details.html', context)