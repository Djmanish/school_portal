from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime



# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=35)
    def __str__(self):
        return self.name

class App_functions(models.Model):
    function_name = models.CharField(max_length= 266, null=True, blank=True, unique=True)
    def __str__(self):
        return self.function_name




class Institute(models.Model):
    name = models.CharField(max_length=150, unique=True )
    profile_pic = models.ImageField(upload_to="Institute Images",default="default_school_pic.jpg" )

    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=150)
    establish_date=models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="Institute Images",default="default_school_pic.jpg" )
    principal = models.CharField(max_length=50, null=True)
    session_start_date = models.DateField(null=True, blank=True)
    about = models.TextField(max_length=300, blank=True, default="This is about Institute" )
    contact_number1 = models.CharField(max_length=12,null=True)
    contact_number2 = models.CharField(max_length=12,null=True, blank=True)
    contact_number3 = models.CharField(max_length=12,null=True, blank=True)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True)
    district=models.CharField(max_length=50,null=True)
    state = models.ForeignKey(to=State, on_delete=models.PROTECT, null= True, blank=True)
    country= models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True)
    about = models.TextField(max_length=300, blank=True, null=True)
    facebook_link=models.URLField(null=True, blank=True, default="Facebook Link")
    website_link=models.URLField(null=True, blank=True, default="Website Link")
    create_date=models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_date=models.DateTimeField(auto_now=True,null=True, blank=True)
    created_by=models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='institute_profile', null=True)


    def __str__(self):
        return self.name




class Institute_levels(models.Model):
    institute= models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institute_levels', null=True, blank=True)
    level_id= models.IntegerField(null=True)
    level_name = models.CharField(max_length=25, null=True, blank=True)
    permissions = models.ManyToManyField(to=App_functions, related_name='user_permissions', null=True, blank=True, )
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    end_date = models.DateField(null=True, blank= True)
    class Meta:
        # unique_together=['institute', 'level_id','level_name']
        ordering = ['-level_id']
    
    def __str__(self):
        return self.level_name





class UserProfile(models.Model):
    Chi1 =[
        ('pending', 'Pending'),('approve', 'Approve'),
        ('dissapprove', 'Dissapprove'),
    ]
    Promotion=[
        ('Promoted', 'Promoted'),
        ('Not Promoted', 'Not Promoted'),
    ]
    gender_choices = [('', '-- select one --'),('Male', 'Male'), ('Female','Female'),('Other','Other')]
    marital_choices = [('','-- select one --'),('Married','Married'),('Unmarried','Unmarried')]
    category_choices =[('','-- select one --'),('Unreserved','Unreserved'),('Sc/St','Sc/St'),('OBC','OBC')]
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')
    institute = models.ForeignKey(to=Institute, related_name="institute", on_delete=models.PROTECT, null=True, blank=True, default="")
    designation = models.ForeignKey('Institute_levels', on_delete=models.PROTECT, related_name='user_designation', null=True)
    Class = models.ForeignKey(to='Classes', on_delete=models.CASCADE,blank=True, null=True, related_name='student_class')
    roll_number = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=25, null=True, default="")
    middle_name = models.CharField(max_length=20, null=True, default="")
    last_name = models.CharField(max_length= 25, null = True,default="")
    father_name = models.CharField(max_length=25, null=True, default="")
    mother_name = models.CharField(max_length=25, null=True, default="")
    gender = models.CharField(max_length=10, choices= gender_choices, null=True, default="" )
    date_of_birth = models.DateField(null= True,  default=date.today)
    marital_status = models.CharField(max_length= 10, choices = marital_choices , default="", null=True)
    category = models.CharField(max_length=10, choices= category_choices , default="", null=True)
    qualification = models.CharField(max_length=200, null=True, default='' )
    aadhar_card_number = models.CharField(max_length= 20, null=True, default='')

    about = models.CharField(max_length=300, blank=True, null=True, default="write something about yourself ")
    profile_pic = models.ImageField(default="default_profile_pic.jpg", upload_to='UserProfilePictures')
    mobile_number = models.PositiveIntegerField(null=True,)
    address_line_1 = models.CharField(max_length= 50 , null= True, default="Address line 1")
    address_line_2 = models.CharField(max_length=50, null = True, default="Address line 2")
    city = models.CharField(max_length=50, null=True, default="City")
    state = models.ForeignKey(to=State, on_delete=models.PROTECT, null= True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True, default="https://www.facebook.com/")
    status = models.CharField(max_length=25,choices=Chi1, null=True)
    class_promotion_status=models.CharField(max_length=30, choices=Promotion, null=True, default="Promoted")
    class_current_year=models.CharField(max_length=30,null=True)
    class_next_year=models.CharField(max_length=30,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def approve(self):
        self.status= 'approve'
        self.save()
    
    def disapprove(self):
        self.status= None
        self.save()

    def __str__(self):
        return str(self.user)





class Role_Description(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user_institute_role', null=True)
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE, related_name='institute_role_desc')
    level = models.ForeignKey(to=Institute_levels, on_delete=models.CASCADE, related_name='level_desc')

    def __str__(self):
        return str(self.level.level_name)

     

class Classes(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE,related_name='institute_classes')
    name =models.CharField(max_length=10,null=True)
    class_teacher= models.ForeignKey(to=User, null=True, on_delete=models.CASCADE,related_name='class_teacher')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    class_stage_choices = [('Primary','Primary'),('Middle','Middle'),('Highschool','Highschool')]
    class_stage = models.CharField(max_length=50, choices= class_stage_choices, null=True)
    # created_by=models.OneToOneField(to=User, on_delete=models.CASCADE, null=True,  related_name='created_by', null=True)
    def __str__(self):
        return str(self.name)

class Subjects(models.Model):
    institute = models.ForeignKey(to=Institute, on_delete=models.CASCADE,related_name='subject_institute', null=True)
    subject_class=models.ForeignKey(to=Classes, on_delete=models.CASCADE, related_name='class_subject', null=True)
    subject_teacher=models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="subject_teacher", null=True)
    subject_code=models.CharField(max_length=100)
    subject_name=models.CharField(max_length=100)

    def __str__(self):
        return str(self.subject_name)




class Tracking_permission_changes(models.Model):
    
    institute = models.ForeignKey(to=Institute, on_delete=models.DO_NOTHING,related_name='institute_role_permission_updated', null=True, blank=True)
    
    role =  models.ForeignKey(to=Institute_levels, on_delete=models.DO_NOTHING, related_name='role_permission_updated', null=True, blank=True)

    update_time = models.DateTimeField()
    changes_made_by = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='user_made_changes_permission')
    
    old_permissions = models.ManyToManyField(to=App_functions, related_name='old_permissions', null=True, blank=True)
    
    updated_permissions = models.ManyToManyField(to=App_functions, related_name='new_permissions', null=True, blank=True)

    comment = models.TextField(null=True, blank=True)


    def __str__(self):
        return str(self.update_time)
            