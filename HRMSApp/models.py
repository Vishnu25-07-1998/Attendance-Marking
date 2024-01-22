from django.db import models

# Create your models here.


class EmployeeDetail(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    doj = models.DateField()
    
    def __str__(self):
        return self.name
    
    
class Employee(models.Model):
    employee = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    work_duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {'Present' if self.is_present else 'Absent'}"
    
    
    
    
    
