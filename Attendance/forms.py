from django.forms import ModelForm
from main_app.models import UserProfile, Student_Info
from django import forms



class Student_profile_edit_form(ModelForm):

    middle_name = forms.CharField(max_length=25, required=False)
    
    profile_pic = forms.FileInput()

    class Meta:
        model = UserProfile
        exclude = ['user','institute','designation','Class','status','class_promotion_status','class_current_year','class_next_year','created_at','updated_at','qualification']
    
        widgets = {
        'date_of_birth':forms.DateInput(attrs={'type':'date'})
        #   'profile_pic': forms.FileField(),
         
        }
        labels ={
            'date_of_birth':'Date of Birth', 'roll_number':'Roll No.', 'first_name':'First Name', 'middle_name':'Middle Name','last_name':'Last Name',"father_name":"Fathers's Name","mother_name":"Mother's Name","marital_status":"Marital Status","aadhar_card_number":"Aadhar Card No.","profile_pic":"Profile Picture","mobile_number":"Contact No.","address_line_1":"Address Line 1","address_line_2":"Address Line 2","pin_code":"PIN Code","facebook_link":"Facebook Profile Link",
        }
  

class Student_info_edit_form(ModelForm):
    
    class Meta:
        model = Student_Info
        exclude = ['student']

        labels = {
            "student_blood_group":"Blood Group","sub_cast":"Sub Caste","f_mobile_Number":"Father's Contact No.","f_Email_Id":"Father's Email","f_aadhar_card":"Father's Aadhar Card No.","f_qualification":"Father's Qualification","f_occupation":"Father's Occupation","f_photo":"Father's Photo","m_mobile_Number":"Mother's Contact No.","m_Email_Id":"Mother's Email","m_aadhar_card":"Mother's Aadhar Card No.","m_qualification":"Mother's Qualification","m_occupation":"Mother's Occupation","m_photo":"Mother's Photo","guardian_name":"Guardian's Name","guardian_mobile_Number":"Guardian's Contact No.","guardian_Email_Id":"Guardian's Email","guardian_aadhar_card":"Guardian's Aadhar Card","guardian_qualification":"Guardian's Qualification","guardian_occupation":"Guardian's Occupation","guardian_photo":"Guardian's Photo","c_address":"Current Address","c_District":"Current City",'c_state':'Current State','c_country':'Current Country','c_Pin_Code':'Current PIN Code','p_address':'Permanent Address','p_district':'Permanent City','p_State':'Permanent State','p_country':'Permanent Country','p_pin_code':'Permanent PIN Code','dob_certificate':'Date of Birth Certificate','id_proof_certificate':'ID Proof Certificate','domicile_certificate':'Domicile Certificate','cast_certificate':'Caste Certificate','character_certificate':'Character Certificate','medical_certificate':'Medical Certificate','transfer_certificate':'Transfer Certificate','last_year_certificate':'Last Year Certificate'
        }