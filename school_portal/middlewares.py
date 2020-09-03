from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import resolve
from django.contrib.auth import logout
class user_approve_middleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
   



    def __call__(self, request):
        current_url_name = resolve(request.path_info).url_name

        if current_url_name == 'auth_logout': # if url is logout then exempted
            redirect('auth_logout')
            
        if request.user.is_authenticated:
            user_status = request.user.profile.status
            if request.user.is_staff: #checking if user has staff status
                pass
            else:
                if current_url_name == 'auth_logout': # if url is logout then exempted
                    pass
                else:
                    if user_status== 'pending':
                        messages.info(request, f'Hello! {request.user.username}, Your Institute {request.user.profile.institute} has not approved your request yet. Once they approve it you will be able to access your account.')
                        return render(request, 'main_app/dashboard.html')
                    
                    
                
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response