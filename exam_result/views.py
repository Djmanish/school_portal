from django.shortcuts import render

# Create your views here.
def exam_result(request):
     return render(request, 'teacher_view.html')