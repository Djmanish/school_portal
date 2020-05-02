from django.shortcuts import render, redirect, HttpResponse
from main_app.models import Classes, UserProfile
from django.contrib import messages
from .models import School_tags, Fees_tag_update_history, Fees_Schedule, Account_details, Student_Tags_Record, Student_Tag_Processed_Record
from django.views.generic import UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import Fees_tag_update_form
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
import datetime
from AddChild.models import *
from fees.models import *
from paytm import checksum
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

def fees_home(request):
    total_tags = School_tags.objects.filter(institute= request.user.profile.institute) # total tags of the school
    all_classes = Classes.objects.filter(institute= request.user.profile.institute)

    if request.method == "POST":
        total_tags_for_s = School_tags.objects.filter(institute= request.user.profile.institute)
        selected_class = Classes.objects.get(pk = request.POST.get('selected_class_'))
        all_students = UserProfile.objects.filter(institute= request.user.profile.institute, Class= selected_class, designation__level_name='student')
        selected_tag = School_tags.objects.get(pk=request.POST.get('selected_tag'))
        
        if selected_class.class_teacher != request.user:
            messages.error(request, 'Only class teacher can map tags !!!')
            return redirect('fees_home')
        if len(total_tags_for_s)<= 0:
             messages.error(request, 'No tags for this institute. First Create a tag.')
             return redirect('fees_home')
        
        if len(all_students)<1:
            messages.error(request, 'No student found in the selected class')
            return redirect('fees_home')

        for student in all_students: #highlighting students that already mapped to this tag
            try:
                student_all_tags = student.student_tags.tags.all()
                if selected_tag in student_all_tags:
                    student.already= "true"
            except:
                pass

        context= {'all_students':all_students,
        'all_tags': total_tags,
         'all_classes': all_classes,
         'showing_student_for_class':selected_class,
         'selected_tag':selected_tag,
         }
        return render(request, 'fees/fees.html', context)

    context= {
        'all_classes': all_classes,
        'all_tags': total_tags
    }
    return render(request, 'fees/fees.html', context)


def parent_fees(request):
    if request.user.profile.designation.level_name == "parent":
        #starting those data for pending fees            
            user_children= AddChild.objects.filter(institute= request.user.profile.institute, parent= request.user.profile)
            parent_student_list = []
            for st in user_children: #select student form add child table
                student= UserProfile.objects.get(pk=st.child.id)
                parent_student_list.append(student)

            if(len(user_children)>0):
                student_fees = Students_fees_table.objects.filter(institute = request.user.profile.institute, student__in= parent_student_list, total_due_amount__gt=0 )
                user_child_fee_status = student_fees             
           
        #Ending those data for pending fees
        # starting those data for payment completed and invoice pdf 
         
            if(len(user_children)>0):
                payment_record = list(reversed(Students_fees_table.objects.filter(institute = request.user.profile.institute, student__in= parent_student_list, total_due_amount=0)))
                
            paginator = Paginator(payment_record, 35)
            page_number = request.GET.get('page')
            payment_history = paginator.get_page(page_number)
                    

        # starting those data for payment completed and invoice pdf    
            context = {'children_fee_status':user_child_fee_status,
            'payment_history':payment_history}
            return render(request, 'fees/parent_fees.html', context)


def creating_tags(request):
    if request.method == "POST":
        fee_code = request.POST.get('fee_code').strip()
        description = request.POST.get('tag_descripton').strip()
        type = request.POST.get('tag_type').strip()
        active_status = request.POST.get('active_status').strip()
        amount = float( request.POST.get('amount').strip())
        tax_percentage = request.POST.get('tax_per').strip()
        start_date = request.POST.get('start_d').strip()
        end_date = request.POST.get('end_d').strip()
        tax_value = (float(amount)*float(tax_percentage))/100
        amount_with_tax = float(amount) + float(tax_value)
        
        try:
            School_tags.objects.get(institute =request.user.profile.institute, fees_code=fee_code)
            messages.error(request, "Tag with this fees code already exists !!!")
            return redirect('fees_home')
        except:
            try:
                School_tags.objects.create(institute= request.user.profile.institute, fees_code= fee_code, description= description, type= type, active=active_status, amount= amount, tax_percentage= tax_percentage, amount_including_tax= amount_with_tax, start_date= start_date, end_date= end_date)
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
        
        new_amount= form.instance.amount + ((form.instance.amount*form.instance.tax_percentage)/100) # updating amount with tax in case of tag update    
        form.instance.amount_including_tax = new_amount

        # creating history update
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

        #starting checking if account details provided
        try:
            accnt_details = Account_details.objects.get(institute = request.user.profile.institute)
        except:
            messages.info(request,'please provide your paytm merchant ID and merchant KEY first in order to proceed further !!!')
            return redirect('fees_home')
        #ending checking if account details provided
        notification_date = request.POST.get('notification_date')
        due_date = request.POST.get('due_date')
        processing_date = request.POST.get('processing_date')
        current_date = str(datetime.date.today())
        if notification_date< current_date or processing_date < current_date or due_date<current_date:
            messages.info(request, "Notification, Due or Process dates can not be past dates.")
            return redirect('fees_home')
        

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
        merchant_id = request.POST.get('merchant_id').strip()
        merchant_key = request.POST.get('merchant_key').strip()
        if len(merchant_key)<16:
            messages.info(request, 'please enter 16 character correct merchant key !!! ')
            return redirect('fees_home')
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
        selected_tag = School_tags.objects.get(pk = request.POST.get('selected_taga'))
        students_list = [] # list of all students selected
        students_class = Classes.objects.get(pk= request.POST.get('students_class'))
        
        selected_students = request.POST.getlist('selected_students')
        for student in selected_students:
            get_student = UserProfile.objects.get(pk = student)
            students_list.append(get_student)
        
        for student in students_list: #creating student record if not existing
            try:
                Student_Tags_Record.objects.get(student= student)
            except:
                Student_Tags_Record.objects.create(institute= request.user.profile.institute, student= student, student_class= student.Class)

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
                student_tags_list = student_tags_list + f"<tr><td colspan='2' >{tag.fees_code}</td><td colspan='2' >{tag.description}</td></tr>"
            if student_tags_list =="":
                student_tags_list = "<tr><td colspan='4' style='color:red;'>No Tags Found for the selected student</td></tr>"
                return HttpResponse(student_tags_list)

            return HttpResponse(student_tags_list)
        else:
            student_tags_list = "<tr colspan='4'><td style='color:red;' >No Tags Found for the selected student</td></tr>"
            return HttpResponse(student_tags_list)
    except:
        student_tags_list = "<tr><td colspan='4' style='color:red;'>No Tags Found for the selected student</td></tr>"
        return HttpResponse(student_tags_list)


def students_mapped_to_a_tag(request):
    
    selected_tag = School_tags.objects.get(pk= request.POST.get('selected_tag'))
    all_students =  selected_tag.tags_to_student.all()
    student_response = ""
    for student in all_students:
        student_response = student_response + f"<option>{student.student.first_name} {student.student.middle_name} {student.student.last_name} - {student.student.Class} </option>"   
    
    return HttpResponse(student_response)      
    

def processing_fees(request):
    try:
        school_students = Student_Tags_Record.objects.filter(institute= request.user.profile.institute)
    except:
        messages.info(request, "No student to process fees")
    
    # starting checking if data already processed
    if_already = Student_Tag_Processed_Record.objects.filter(institute = request.user.profile.institute, due_date = request.user.profile.institute.institute_schedule.due_date ).first()
    if if_already:
        return HttpResponse('fees already processed for this due date')
    # ending checking if data already processed


    for st in school_students:          
        for tag in st.tags.all():
            if tag.active == "yes":
                if str(tag.start_date)< str(st.student.institute.institute_schedule.due_date) < str(tag.end_date):
                    Student_Tag_Processed_Record.objects.create(institute= st.student.institute, 
                    notification_date = st.student.institute.institute_schedule.notification_date, 
                    process_date = st.student.institute.institute_schedule.processing_date,
                    due_date = st.student.institute.institute_schedule.due_date,
                    student= st.student,
                    fees_code = tag.fees_code,
                    description = tag.description,
                    type = tag.type,
                    active= tag.active,
                    amount = tag.amount,
                    tax_percentage = tag.tax_percentage,
                    amount_including_tax = tag.amount_including_tax,
                    start_date = tag.start_date,
                    end_date = tag.end_date
                        )  

    # removing schedule, notification and due date of institute
    institute_dates = Fees_Schedule.objects.get(institute= request.user.profile.institute)
    institute_dates.delete()
    return HttpResponse("")



def fees_pay_page(request):
    if request.method == "POST":

        # starting fetching account details
        try:
            accnt_details = Account_details.objects.get(institute = request.user.profile.institute)
        except:
            messages.info(request,'your Institute has not provided account details to complete this payment!!!   ')
            return redirect('parent_fees')
        merchant_id = accnt_details.merchant_id
        MERCHANT_KEY = accnt_details.merchant_key
        # ending fetching account details
        
        
        student_id = request.POST.get('s_id')
      
        amount = request.POST.get('s_amount')
        invoice_no = request.POST.get('s_inv')
        param_dict = {
        # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        "MID" : merchant_id,

        # Find your WEBSITE in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        "WEBSITE" : "WEBSTAGING",

        # Find your INDUSTRY_TYPE_ID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        "INDUSTRY_TYPE_ID" : "Retail",

        # WEB for website and WAP for Mobile-websites or App
        "CHANNEL_ID" : "WEB",

        # Enter your unique order id
        "ORDER_ID" : str(invoice_no),

        # unique id that belongs to your customer
        "CUST_ID" : str(student_id),

        # customer's mobile number
        "MOBILE_NO" : '8090831662',

        # customer's email
        "EMAIL" : 'writetodhananjay@gmail.com' ,

        # Amount in INR that is payble by customer
        # this should be numeric with optionally having two decimal points
        "TXN_AMOUNT" : str(amount),

        # on completion of transaction, we will send you the response on this URL
        "CALLBACK_URL" : "http://trueblueappworks.com//fees/handle_requests/",
    }

        # MERCHANT_KEY = "#OqHWC23DZX1G2LN"
        
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)

        return render(request, 'fees/payment_page.html', {'param_dict':param_dict})



@csrf_exempt
def handle_requests(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            Checksum = form[i]
        
     # starting fetching account details
    institute_id_d = str(response_dict['ORDERID'])
    new_d = institute_id_d.split('-')
    school_id = new_d[0]
    accnt_details = Account_details.objects.get(institute__id = school_id)
    MERCHANT_KEY = accnt_details.merchant_key
    # ending fetching account details
        
    MERCHANT_KEY = accnt_details.merchant_key
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, Checksum )
    if verify:
        if response_dict['RESPCODE'] == '01':
            invoice__num = response_dict['ORDERID']
            user = Students_fees_table.objects.get(invoice_number=invoice__num)
            user.total_due_amount = float(user.total_due_amount) - float(response_dict['TXNAMOUNT'])
            user.total_paid = response_dict['TXNAMOUNT']
            user.payment_date = timezone.now()
            user.balance = float(user.total_due_amount) - float(response_dict['TXNAMOUNT'])
            user.save()
        else:
            print('order was not successfull because ' + response_dict['RESPMSG'])
    
    user_response_dict = {}
    for k,v in response_dict.items():
        if k=="MID":
            pass
        else:
            user_response_dict[k]=v
            
    return render(request, 'fees/payment_status.html', {'response':user_response_dict, })
        

#function for payment details view link
def view_invoice(request, pk):
    fee_data = Students_fees_table.objects.get(pk=pk)
    procees_table_data = Student_Tag_Processed_Record.objects.filter(institute= request.user.profile.institute, due_date = fee_data.due_date, student = fee_data.student)

    total_sum_including_tax = 0
    total_sum_amount = 0
    for am in procees_table_data:
        total_sum_including_tax = total_sum_including_tax + am.amount_including_tax
        total_sum_amount = total_sum_amount + am.amount
    
    tax_amount = total_sum_including_tax - total_sum_amount
    
    if fee_data.total_due_amount == 0:
        payment_status = True
        payment_date = fee_data.payment_date
    else:
        payment_status = False
        payment_date = None
    


    context = {
        'fee_data':fee_data,
        'fee_proce_data':procees_table_data,
        'tax_amount':tax_amount,
        'payment_status':payment_status,
        'payment_date':payment_date

    }
    return render(request, 'fees/invoice.html', context)