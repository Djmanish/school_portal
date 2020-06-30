from django.db import models
from django.core.validators import validate_email, RegexValidator
from main_app.models import *
from django.contrib.auth.models import User

# Create your models here.

class Admission_Query(models.Model):
    
    first_name = models.CharField(max_length=20, verbose_name="First Name",)
    middle_name =  models.CharField(max_length=20, blank= True, null= True, )
    last_name =  models.CharField(max_length=20, blank= True, null= True, )
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(choices = [('Male','Male'), ('Female','Female'),('Other','Other')], max_length=9, null=True)
    school_name = models.ForeignKey(to=Institute, null=True, on_delete= models.SET_NULL, )
    class_name = models.ForeignKey(to=Classes, null=True, on_delete=models.SET_NULL, related_name='requested_school_class')
    mobile_Number =models.CharField( max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], null=True)
    Email_Id = models.CharField(validators=[validate_email], max_length=100,blank= True, null= True,)
    student_aadhar_card = models.CharField(max_length= 20, null=True, default='')
    student_blood_group = models.CharField(choices = [('A+','A+'), ('B+','B+'),('AB+','AB+'),('O+','O+'),('A-','A-'),('B-','B-'),('AB-','AB-'),('O-','O-')], max_length=9, null=True)
    # Nationality = models.CharField(choices = [('Indian','Indian'), ('Other','Other')],  max_length=10, null=True)
    
    Address = models.CharField(max_length=100, null=True)
    District = models.CharField(max_length=20, null=True)
    State = models.CharField(max_length=20, null=True )
    country= models.CharField(max_length=100, null=True, blank=True)
    Pin_Code = models.IntegerField(null=True)

    p_address = models.CharField(max_length=100, null=True)
    p_district = models.CharField(max_length=20, null=True)
    p_State = models.CharField(max_length=20, null=True )
    p_country= models.CharField(max_length=100, null=True, blank=True)
    p_pin_code = models.IntegerField(null=True)
    address_same = models.BooleanField(null=True)
    religion = models.CharField(choices = [('Hindu','Hindu'), ('Islam','Islam'),('Sikhs','Sikhs'),('Christain','Christain'),('Bhudhist','Bhudhist'),('Jain','Jain'),('Other','Other')], max_length=15, null=True)
    category = models.CharField(choices = [('General','General'),('SC/ST','SC/ST'), ('OBC','OBC') ],  max_length=10, null=True)
    sub_cast = models.CharField(max_length=100, null=True, blank=True)
    Student_Photo = models.ImageField( upload_to='Student_Photos', null=True)
    father_name = models.CharField(max_length=30, null=True)
    f_mobile_Number =models.CharField( max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], null=True)
    f_Email_Id = models.CharField(validators=[validate_email], max_length=100,blank= True, null= True,)
    f_aadhar_card = models.CharField(max_length= 20, null=True, default='')
    f_qualification = models.CharField(max_length=20, null=True)
    f_occupation = models.CharField(max_length=20, null=True)
    f_photo = models.ImageField( upload_to='student_document', null=True)
    mother_name = models.CharField(max_length=30, null=True)
    m_mobile_Number =models.CharField( max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], null=True)
    m_Email_Id = models.CharField(validators=[validate_email], max_length=100,blank= True, null= True,)
    m_aadhar_card = models.CharField(max_length= 20, null=True, default='')
    m_qualification = models.CharField(max_length=20, null=True)
    m_occupation = models.CharField(max_length=20, null=True)
    m_photo = models.ImageField( upload_to='student_document', null=True)
    guardian_name = models.CharField(max_length=30, null=True)
    g_mobile_Number =models.CharField( max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], null=True)
    g_Email_Id = models.CharField(validators=[validate_email], max_length=100,blank= True, null= True,)
    g_aadhar_card = models.CharField(max_length= 20, null=True, default='')
    g_qualification = models.CharField(max_length=20, null=True)
    g_occupation = models.CharField(max_length=20, null=True)
    g_photo = models.ImageField( upload_to='student_document', null=True)
    g_applicable = models.BooleanField(null=True)

    dob_certificate = models.FileField( upload_to='student_document', null=True)
    id_proof_certificate = models.FileField( upload_to='student_document', null=True)
    domicile_certificate = models.FileField( upload_to='student_document', null=True)
    cast_certificate = models.FileField( upload_to='student_document', null=True)
    character_certificate = models.FileField( upload_to='student_document', null=True)
    medical_certificate = models.FileField( upload_to='student_document', null=True)
    transfer_certificate = models.FileField( upload_to='student_document', null=True)
    last_year_certificate = models.FileField( upload_to='student_document', null=True)
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Disapproved', 'Disapproved'),
       
    ]

    status = models.CharField(max_length=15, choices = STATUS_CHOICES, default="Pending")
    request_by = models.OneToOneField(to=User, null=True, on_delete=models.SET_NULL, related_name='admission_request')
    
   
    def __str__(self):
        return f"{self.first_name} "
