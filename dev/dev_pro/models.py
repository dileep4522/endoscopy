from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patientsdetails(models.Model):
    objects = None
    DoesNotExist = None
    patient_name = models.CharField(max_length=100,null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=15,null=False)
    procedure = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=20,null=False,unique=True)
    patient_email = models.EmailField(unique=True)
    referred = models.CharField(max_length=100)

    def __str__(self):
        return str(self.patient_name)


class Patientreports(models.Model):
    def nameFile(instance, filename):
        return '/'.join(['endo_files', str(instance.patient_details_id), filename])
    patient_details_id = models.ForeignKey(Patientsdetails,on_delete=models.CASCADE,related_name="Patient_reports")
    report_file = models.FileField(upload_to=nameFile,blank=True)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.patient_details_id)


class UserDetails(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15,null=False)
    speciality = models.CharField(max_length=50,blank=False)
    otp = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.user_id)

