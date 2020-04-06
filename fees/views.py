from django.shortcuts import render, redirect, HttpResponse
from main_app.models import Classes, UserProfile
from django.contrib import messages
from .models import School_tags, Fees_tag_update_history, Fees_Schedule, Account_details, Student_Tags_Record
from django.views.generic import UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import Fees_tag_update_form
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

def fees_home(request):
    
    total_tags = School_tags.objects.filter(institute= request.user.profile.institute) # total tags of the school
    
    all_classes = Classes.objects.filter(institute= request.user.profile.institute)

    if request.method == "POST":
        total_tags_for_s = School_tags.objects.filter(institute= request.user.profile.institute)
        selected_class = Classes.objects.get(pk = request.POST.get('selected_class_'))
        all_students = UserProfile.objects.filter(institute= request.user.profile.institute, Class= selected_class, designation__level_name='student')
        
        student_multiple_select_height = all_students.count()*25 # defining size of student select field
        
        if len(all_students)<1:
            messages.error(request, 'No student found in the selected class')
            return redirect('fees_home')
        
        context= {'all_students':all_students,
        'all_tags': total_tags,
         'all_classes': all_classes,
         'showing_student_for_class':selected_class,
         'total_tags_for_s':total_tags_for_s,
         'student_multiple_select_height':student_multiple_select_height
         }
        return render(request, 'fees/fees.html', context)
        
        
    context= {
        'all_classes': all_classes,
        'all_tags': total_tags
    }
    return render(request, 'fees/fees.html', context)


def parent_fees(request):
    return render(request, 'fees/parent_fees.html')




def creating_tags(request):
    if request.method == "POST":
        fee_code = request.POST.get('fee_code').strip()
        description = request.POST.get('tag_descripton').strip()
        type = request.POST.get('tag_type').strip()
        active_status = request.POST.get('active_status').strip()
        amount = request.POST.get('amount').strip()
        tax_percentage = request.POST.get('tax_per').strip()
        start_date = request.POST.get('start_d').strip()
        end_date = request.POST.get('end_d').strip()
        
        try:
            School_tags.objects.get(fees_code=fee_code)
            messages.error(request, "Tag with this fees code already exists !!!")
            return redirect('fees_home')
        except:
            try:
                School_tags.objects.create(institute= request.user.profile.institute, fees_code= fee_code, description= description, type= type, active=active_status, amount= amount, tax_percentage= tax_percentage, start_date= start_date, end_date= end_date)
                messages.success(request, 'Tag Created Successfully !!!')
                return redirect('fees_home')
            except:
                messages.error(request, 'Could not create this tag. please try again !!!')
                return redirect('fees_home')


class Fees_tag_update_view(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = School_tags
    # fields = ['fees_code','description','type','active','amount','tax_percentage','start_date','end_date']
    form_class = Fees_tag_update_form
    template_name = 'fees/edit_fees_tag.html'
    success_url = "/fees"
    success_message = "Fees Tag information updated successfully !!!"
    
    def form_valid(self, form):
        tag_id = self.get_object().id
        old_tag = School_tags.objects.get(pk=tag_id)
        old_tag_values = f"Fees Code: {old_tag.fees_code}, Description: {old_tag.description}, Type: {old_tag.type}, Active_status:{old_tag.active}, Amount: {old_tag.amount}, Tax Percentage:{old_tag.tax_percentage}, Start Date: {old_tag.start_date}, End Date:{old_tag.end_date}"

        updated_values= f"Fees Code: {form.instance.fees_code}, Description: {form.instance.description}, Type: {form.instance.type}, Active_status:{form.instance.active}, Amount: {form.instance.amount}, Tax Percentage:{form.instance.tax_percentage}, Start Date: {form.instance.start_date}, End Date:{form.instance.end_date}"

        new_update_record = Fees_tag_update_history()
        new_update_record.fees_tag = old_tag
        new_update_record.date = timezone.now()
        new_update_record.update_by = self.request.user
        new_update_record.old_values = old_tag_values
        new_update_record.new_values = updated_values
        new_update_record.save()
        return super().form_valid(form)
    
class Fees_Tag_History_List(LoginRequiredMixin, ListView):
    model = Fees_tag_update_history
    template_name = 'fees/fees_tag_update_history.html'
    paginate_by = 20
    

def institute_fees_schedule(request):
    if request.method == "POST":
        notification_date = request.POST.get('notification_date')
        due_date = request.POST.get('due_date')
        processing_date = request.POST.get('processing_date')

        try:
            check_existance = Fees_Schedule.objects.get(institute = request.user.profile.institute)
            check_existance.institute = request.user.profile.institute
            check_existance.notification_date= notification_date
            check_existance.due_date= due_date
            check_existance.processing_date= processing_date
            check_existance.save()
            messages.info(request, 'Fees Schedule updated !!!')
            return redirect('fees_home')
        except:
            Fees_Schedule.objects.create(institute = request.user.profile.institute, notification_date= notification_date, due_date= due_date, processing_date= processing_date)
            messages.success(request, 'Schedule Information Updated !!!')
            return redirect('fees_home')

def institute_account_details(request):
     if request.method == "POST":
        merchant_id = request.POST.get('merchant_id')
        merchant_key = request.POST.get('merchant_key')
        try:
            check_existence_ad = Account_details.objects.get(institute = request.user.profile.institute)
            
            check_existence_ad.merchant_id = merchant_id
            check_existence_ad.merchant_key = merchant_key
            check_existence_ad.save()
            messages.info(request, 'Account Details Updated Successfully !!!')
            return redirect('fees_home')
        except:
            
            Account_details.objects.create(institute = request.user.profile.institute, merchant_id = merchant_id, merchant_key = merchant_key)
            messages.success(request, 'Account Details Updated Successfully !!!')
            return redirect('fees_home')


def Map_Tag_Students(request):
    if request.method == "POST":
        selected_tag = School_tags.objects.get(pk = request.POST.get('selected_tag'))
        students_list = [] # list of all students selected
        students_class = Classes.objects.get(pk= request.POST.get('students_class'))
        print(students_class)
        
        selected_students = request.POST.getlist('selected_students')
        for student in selected_students:
            get_student = UserProfile.objects.get(pk = student)
            students_list.append(get_student)
        
        for student in students_list: #creating student record if not existing
            try:
                Student_Tags_Record.objects.get(student= student)
            except:
                Student_Tags_Record.objects.create(student= student, student_class= student.Class)

    #    removing this tag from all students in case of update
        students_with_this_tag = Student_Tags_Record.objects.filter(student_class= students_class)
        for student in students_with_this_tag:
            student.tags.remove(selected_tag)
        
        
        for student in students_list:
            fetch_student = Student_Tags_Record.objects.get(student = student)
            fetch_student.tags.add(selected_tag)
        return redirect('fees_home')


def Fetch_student_for_tags(request):
    selected_class = Classes.objects.get(pk = request.POST.get('selected_class_'))
    all_students = UserProfile.objects.filter(institute= request.user.profile.institute, Class= selected_class, designation__level_name='student')
    students_response = "<option selected disabled value=''> --- select a student ---</option>"
    for student in all_students:
        students_response = students_response + f"<option value='{student.id}''>{student.first_name} {student.middle_name} {student.last_name}</option>"  
    return HttpResponse(students_response)  


def fetch_students_tags_mapped(request):
    selected_student = UserProfile.objects.get(pk = request.POST.get('student_id'))
    try:
        student_tags = Student_Tags_Record.objects.get(student= selected_student)
        if student_tags:
            student_tags_list = ""
            for tag in student_tags.tags.all():
                student_tags_list = student_tags_list + f"<tr><td>{tag.fees_code}</td><td>{tag.description}</td></tr>"
            if student_tags_list =="":
                student_tags_list = "<tr><td colspan='2'>No Tags Found for the selected student</td></tr>"
                return HttpResponse(student_tags_list)

            return HttpResponse(student_tags_list)
        else:
            student_tags_list = "<tr><td colspan='2'>No Tags Found for the selected student</td></tr>"
            return HttpResponse(student_tags_list)
    except:
        student_tags_list = "<tr><td colspan='2'>No Tags Found for the selected student</td></tr>"
        return HttpResponse(student_tags_list)

                
    
        