from django.shortcuts import render, HttpResponse
from .models import *
from main_app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import *

# Create your views here.

@login_required
def schedule(request):
    select_class_for_schedule = request.GET.get('selected_class') # class selected to view
    if select_class_for_schedule == None:
            first_class = Classes.objects.filter(institute= request.user.profile.institute).first()
            first_class_id = first_class.id
            select_class_for_schedule= first_class_id
            

    selected_class = Classes.objects.get(pk=select_class_for_schedule) #fetching the class instance seleted to view

    all_class = Classes.objects.filter(institute=request.user.profile.institute)
    all_lectures = Lecture.objects.filter(institute=request.user.profile.institute)
    

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
                'saturday_schedule':saturday_schedule

                }
   
    return render(request, 'class_schedule/schedule.html', context)


def schedule_update(request, pk):
        schedule_to_update = Schedule.objects.get(pk=pk) # fetching schedule instance to update
        
        institute_subjects = Subjects.objects.filter(institute= request.user.profile.institute, subject_class= schedule_to_update.Class) # fetching available subjects in the institute

        institute_teachers = UserProfile.objects.filter(institute=request.user.profile.institute)

        context_data = {'schedule_info':schedule_to_update,
                        'all_subjects':institute_subjects,
                        'institute_teachers': institute_teachers}
        if request.method == "POST":
                
                schedule_to_update.subject_lecture_one = Subjects.objects.get(pk=request.POST.get('subject_lecture_one'))
                schedule_to_update.subject_teacher_lecture_one= User.objects.get(pk=request.POST.get('subject_teacher_lecture_one'))

                schedule_to_update.subject_lecture_two = Subjects.objects.get(pk=request.POST.get('subject_lecture_two'))
                schedule_to_update.subject_teacher_lecture_two=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_two'))

                schedule_to_update.subject_lecture_three= Subjects.objects.get(pk=request.POST.get('subject_lecture_three'))
                schedule_to_update.subject_teacher_lecture_three=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_three'))

                schedule_to_update.subject_lecture_four= Subjects.objects.get(pk=request.POST.get('subject_lecture_four'))
                schedule_to_update.subject_teacher_lecture_four=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_four'))

                schedule_to_update.subject_lecture_five= Subjects.objects.get(pk=request.POST.get('subject_lecture_five'))
                schedule_to_update.subject_teacher_lecture_five=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_five'))

                schedule_to_update.subject_lecture_six= Subjects.objects.get(pk=request.POST.get('subject_lecture_six'))
                schedule_to_update.subject_teacher_lecture_six=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_six'))

                schedule_to_update.subject_lecture_seven= Subjects.objects.get(pk=request.POST.get('subject_lecture_seven'))
                schedule_to_update.subject_teacher_lecture_seven=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_seven'))

                schedule_to_update.subject_lecture_eight= Subjects.objects.get(pk=request.POST.get('subject_lecture_eight'))
                schedule_to_update.subject_teacher_lecture_eight=  User.objects.get(pk=request.POST.get('subject_teacher_lecture_eight'))



                schedule_to_update.save()
       
        return render(request, 'class_schedule/update_schedule.html', context_data )