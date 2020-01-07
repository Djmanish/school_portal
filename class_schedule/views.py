from django.shortcuts import render, HttpResponse
from .models import *
from main_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import *
from django.views.generic import ListView, UpdateView
from django.urls import reverse, reverse_lazy
# Create your views here.

@login_required
def schedule(request):
    select_class_for_schedule = request.GET.get('selected_class') # class selected to view
    if select_class_for_schedule == None:
            first_class = Classes.objects.filter(institute= request.user.profile.institute).last()
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


    print(monday_schedule)
    context = {'all_classes': all_class,
                'all_lectures': all_lectures,
                'monday_schedule':monday_schedule,
                'tuesday_schedule':tuesday_schedule,
                'wednesday_schedule':wednesday_schedule,
                'thursday_schedule':thursday_schedule,
                'friday_schedule':friday_schedule,
                'saturday_schedule':saturday_schedule,
                "time_table_for_class": time_table_for_class

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
        if request.method == "POST":
                
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




                schedule_to_update.save()
       
        return render(request, 'class_schedule/update_schedule.html', context_data )
@login_required
def class_stage_lecture_time_update(request):
        return render(request, 'class_schedule/update_lecture_time.html')



class Update_lecture_time(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
        model = Lecture

        fields = ['start_time','end_time']
        template_name= 'class_schedule/update_timing.html'
        success_message = "Timing Updated Successfully !!!"

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

