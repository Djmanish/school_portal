from django.shortcuts import render, HttpResponse, redirect
from .models import *
from main_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import *
from django.views.generic import ListView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from notices.models import Notice
from django.utils import timezone
# Create your views here.

@login_required
def schedule(request):
    # starting user notice
    if request.user.profile.designation:
        teacher_role_level = Institute_levels.objects.get(level_name='teacher', institute= request.user.profile.institute)
        teacher_role_level = teacher_role_level.level_id
        user_role_level = request.user.profile.designation.level_id
        request.user.users_notice = []
        all_notices = Notice.objects.filter(institute=request.user.profile.institute, publish_date__lte=timezone.now()).order_by('id')
        if user_role_level < teacher_role_level:
            request.user.users_notice = all_notices.exclude(category="absent").reverse()
        else:
            for notice in all_notices:
                notice_recipients = notice.recipients_list.all()
                if request.user.profile in notice_recipients:
                    request.user.users_notice.insert(0, notice)
        # ending user notice    
    select_class_for_schedule = request.GET.get('selected_class') # class selected to view
    if select_class_for_schedule == None:
            first_class = Classes.objects.filter(institute= request.user.profile.institute).last()
            if first_class:
                    pass
            else:
                    messages.info(request, 'It seems there are no classes in the institute. First create the classes then you can access schedule')
                    return redirect('user_dashboard')
            first_class_id = first_class.id
            select_class_for_schedule= first_class_id
            

    selected_class = Classes.objects.get(pk=select_class_for_schedule) #fetching the class instance seleted to view

    time_table_for_class = selected_class.name
    selected_class_stage = selected_class.class_stage
    
    all_class = Classes.objects.filter(institute=request.user.profile.institute)
    all_lectures = Lecture.objects.filter(institute=request.user.profile.institute, class_stage= selected_class_stage)
    

    monday_schedule = Schedule.objects.get(institute=request.user.profile.institute, Class= selected_class, day="Monday"  )
    tuesday_schedule = Schedule.objects.get(institute=request.user.profile.institute, Class= selected_class, day="Tuesday" )

    wednesday_schedule = Schedule.objects.get(institute=request.user.profile.institute, Class= selected_class, day="Wednesday" )

    thursday_schedule = Schedule.objects.get(institute=request.user.profile.institute, Class= selected_class, day="Thursday" )

    friday_schedule = Schedule.objects.get(institute=request.user.profile.institute, Class= selected_class, day="Friday" )

    saturday_schedule = Schedule.objects.get(institute=request.user.profile.institute, Class= selected_class, day="Saturday" )

    user_permissions = request.user.user_institute_role.level.permissions.all()
    schedule_update_permission = App_functions.objects.get(function_name='Can Update Schedule')
    update_lecture_timing = App_functions.objects.get(function_name='Can Update Lecture Timing')

    context = {'all_classes': all_class,
                'all_lectures': all_lectures,
                'monday_schedule':monday_schedule,
                'tuesday_schedule':tuesday_schedule,
                'wednesday_schedule':wednesday_schedule,
                'thursday_schedule':thursday_schedule,
                'friday_schedule':friday_schedule,
                'saturday_schedule':saturday_schedule,
                "time_table_for_class": time_table_for_class,
                'user_permissions': user_permissions,
                'schedule_update_permission': schedule_update_permission,
                'update_lecture_timing':update_lecture_timing

                }
   
    return render(request, 'class_schedule/schedule.html', context)

@login_required
def schedule_update(request, pk):

        schedule_to_update = Schedule.objects.get(pk=pk) # fetching schedule instance to update
        
        institute_subjects = Subjects.objects.filter(institute= request.user.profile.institute, subject_class= schedule_to_update.Class) # fetching available subjects in the institute
        teacher_designation_pk = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='teacher')
        institute_teachers = UserProfile.objects.filter(institute=request.user.profile.institute, designation= teacher_designation_pk )

        context_data = {'schedule_info':schedule_to_update,
                        'all_subjects':institute_subjects,
                        'institute_teachers': institute_teachers}

        user_permissions = request.user.user_institute_role.level.permissions.all()
        schedule_update_permission = App_functions.objects.get(function_name='Can Update Schedule')
        

        if request.method == "POST":
                if schedule_update_permission in user_permissions:

                        try:
                                schedule_to_update.subject_lecture_one = Subjects.objects.get(pk=request.POST.get('subject_lecture_one'))
                        except:
                                schedule_to_update.subject_lecture_one =None

                        try:
                                schedule_to_update.subject_teacher_lecture_one= User.objects.get(pk=request.POST.get('subject_teacher_lecture_one'))
                        except:
                                schedule_to_update.subject_teacher_lecture_one=None

                        try:
                                schedule_to_update.subject_lecture_two = Subjects.objects.get(pk=request.POST.get('subject_lecture_two'))
                        except:
                                schedule_to_update.subject_lecture_two = None

                        try:
                                schedule_to_update.subject_teacher_lecture_two=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_two'))
                        except:
                                schedule_to_update.subject_teacher_lecture_two= None

                        try:
                                schedule_to_update.subject_lecture_three= Subjects.objects.get(pk=request.POST.get('subject_lecture_three'))
                        except:
                                schedule_to_update.subject_lecture_three=None

                        try:
                                schedule_to_update.subject_teacher_lecture_three=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_three'))
                        except:
                                schedule_to_update.subject_teacher_lecture_three= None

                        try:
                                schedule_to_update.subject_lecture_four= Subjects.objects.get(pk=request.POST.get('subject_lecture_four'))
                        except:
                                schedule_to_update.subject_lecture_four= None

                        try:
                                schedule_to_update.subject_teacher_lecture_four=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_four'))
                        except:
                                schedule_to_update.subject_teacher_lecture_four= None

                        try:
                                schedule_to_update.subject_lecture_five= Subjects.objects.get(pk=request.POST.get('subject_lecture_five'))
                        except:
                                schedule_to_update.subject_lecture_five= None

                        try:
                                schedule_to_update.subject_teacher_lecture_five=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_five'))
                        except:
                                schedule_to_update.subject_teacher_lecture_five= None

                        try:
                                schedule_to_update.subject_lecture_six= Subjects.objects.get(pk=request.POST.get('subject_lecture_six'))
                        except:
                                schedule_to_update.subject_lecture_six= None

                        try:
                                schedule_to_update.subject_teacher_lecture_six=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_six'))
                        except:
                                schedule_to_update.subject_teacher_lecture_six=  None

                        try:
                                schedule_to_update.subject_lecture_seven= Subjects.objects.get(pk=request.POST.get('subject_lecture_seven'))
                        except:
                                schedule_to_update.subject_lecture_seven= None
                        
                        try:
                                schedule_to_update.subject_teacher_lecture_seven=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_seven'))
                        except:
                                schedule_to_update.subject_teacher_lecture_seven= None

                        try:
                                schedule_to_update.subject_lecture_eight= Subjects.objects.get(pk=request.POST.get('subject_lecture_eight'))
                        except:
                                schedule_to_update.subject_lecture_eight=None
                                
                        try:
                                schedule_to_update.subject_teacher_lecture_eight=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_eight'))
                        except:
                                schedule_to_update.subject_teacher_lecture_eight=None
                        
                        messages.success(request, "Class Schedule Updated Successfully !!!")
                        schedule_to_update.save()
                else:
                        messages.info(request, "You don't have permission to update class Schedule")
                        return redirect('not_found')
        return render(request, 'class_schedule/update_schedule.html', context_data )
@login_required
def class_stage_lecture_time_update(request):
        return render(request, 'class_schedule/update_lecture_time.html')


from .forms import Update_lecture_time_Form
class Update_lecture_time(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
        model = Lecture

        # fields = ['start_time','end_time']
        form_class = Update_lecture_time_Form
        template_name= 'class_schedule/update_timing.html'
        success_message = "Timing Updated Successfully !!!"

        def test_func(self):
                user_permissions = self.request.user.user_institute_role.level.permissions.all()
                update_lecture_timing = App_functions.objects.get(function_name='Can Update Lecture Timing')
                if update_lecture_timing in user_permissions:
                        return True
                else:
                        return False
                

        def get_success_url(self, **kwargs):
                current_object = self.get_object()
                if current_object.class_stage == "Primary":
                        stage_id=1
                elif current_object.class_stage == "Middle":
                        stage_id=2
                else:
                        stage_id=3
                return reverse_lazy("class_stage_lectures", kwargs={'id':stage_id})
        
        
        

def class_stage_all_lectures(request, id):
        if id == 1:
                all_lectures = Lecture.objects.filter(institute=request.user.profile.institute, class_stage='Primary')
                return render(request, 'class_schedule/class_stage_all_lectures.html',{'all_lectures':all_lectures, 'class_stage':'Primary'})
        elif id ==2:
                all_lectures = Lecture.objects.filter(institute=request.user.profile.institute, class_stage='Middle')
                return render(request, 'class_schedule/class_stage_all_lectures.html',{'all_lectures':all_lectures,'class_stage':'Middle'})
        elif id == 3:
                all_lectures = Lecture.objects.filter(institute=request.user.profile.institute, class_stage='Highschool')
                return render(request, 'class_schedule/class_stage_all_lectures.html',{'all_lectures':all_lectures,'class_stage':'Highschool'})

