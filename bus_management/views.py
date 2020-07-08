from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages
from django.utils import timezone
from notices.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import math

# Create your views here.
def bus(request):
    buses = Bus.objects.filter(bus_institute=request.user.profile.institute)
    states_list = State.objects.all()
    points = Point.objects.filter(point_institute=request.user.profile.institute)
    drivers = Driver.objects.filter(institute=request.user.profile.institute)
    active_buses = Bus.objects.filter(bus_institute=request.user.profile.institute, status="active")
    routes = RouteInfo.objects.filter(institute=request.user.profile.institute)
    context_data = {
        'buses': buses,
        'states_list': states_list,
        'points':points,
        'drivers':drivers,
        'active_buses':active_buses,
        'routes':routes,
    }
    return render(request, 'bus/bus_management.html', context_data)

def add_bus(request):
    if request.method == 'POST':
        b_no= request.POST['bus_no'].strip().upper() 
        b_maker= request.POST['bus_maker'].strip()
        b_type= request.POST['bus_type'].strip()
        b_fuel = request.POST['bus_fuel_type']
        b_color= request.POST['bus_color'].strip()
        b_capacity= request.POST['bus_capacity'].strip()
        print(b_no)
        try:
            chk_bus= Bus.objects.get(bus_no=b_no, bus_institute=request.user.profile.institute)
            messages.error(request, 'Bus Is Already Exists !')
            return HttpResponseRedirect(f'/bus/')    
        except Bus.DoesNotExist:
            new_bus = Bus.objects.create(bus_no=b_no, bus_maker=b_maker, vehicle_type=b_type,fuel_type=b_fuel, bus_color=b_color, bus_capacity=b_capacity, bus_institute=request.user.profile.institute)
            messages.success(request, 'Bus Added successfully !')  
            return HttpResponseRedirect(f'/bus/')

def edit_bus(request):
    if request.method == 'POST':
        b_id = request.POST['edit_bus_id']
        srch_bus = Bus.objects.get(id=b_id)
        bb_no = request.POST['edit_bus_n'].strip().upper()
        srch_bus.bus_no = bb_no
        srch_bus.bus_maker = request.POST['edit_maker'].strip()
        srch_bus.fuel_type = request.POST['edit_fuel'].strip()
        srch_bus.vehicle_type = request.POST['edit_bus_typ'].strip()
        srch_bus.bus_color = request.POST['edit_bus_colo'].strip()
        srch_bus.bus_capacity = request.POST['edit_bus_capacit'].strip()
        srch_bus.save()
        messages.success(request, 'Bus Info Updated Successfully !')  
        return HttpResponseRedirect(f'/bus/')



def add_point(request):
    if request.method == 'POST':
        p_code = request.POST['point_code'].strip()
        p_name = request.POST['point_name'].strip()
        p_street_no = request.POST['point_street'].strip()
        p_landmark = request.POST['point_landmark'].strip()
        p_place = request.POST['point_place'].strip()
        p_city = request.POST['point_city'].strip()
        p_state = request.POST['point_state']
        sel_state = State.objects.get(pk=p_state)
        print(sel_state)
        p_country = request.POST['point_country'].strip()
        print("Hello")
        try:
            chk_point= Point.objects.get(point_code=p_code, point_institute=request.user.profile.institute)
        except Point.DoesNotExist:
            chk_point = 0 
        if chk_point == 0:
            new_point = Point.objects.create(point_code=p_code, point_name=p_name, point_street_no=p_street_no, point_landmark=p_landmark,point_exact_place=p_place, point_city=p_city, point_state=sel_state, point_country=p_country,  point_institute=request.user.profile.institute)
            messages.success(request, 'Point Created successfully !')  
            return HttpResponseRedirect(f'/bus/')       
        else:
            messages.error(request, 'Point Is Already Exists !')
            return HttpResponseRedirect(f'/bus/') 

def edit_point(request):
    if request.method == 'POST':
        selected_point = request.POST['edit_point_id_hide']
        point = Point.objects.get(pk=selected_point)
        p_state = request.POST['edit_point_state']
        state = State.objects.get(pk=p_state)
        point.point_code= request.POST['edit_point_code']
        point.point_name = request.POST['edit_point_name']
        point.point_street_no = request.POST['edit_point_street']
        point.point_landmark = request.POST['edit_point_landmark']
        point.point_exact_place = request.POST['edit_point_place']
        point.point_city = request.POST['edit_point_city']
        point.point_state = state
        point.point_country = request.POST['edit_point_country']
        point.save()
        messages.success(request, 'Point Details Updated successfully !')  
        return HttpResponseRedirect(f'/bus/') 

def delete_point(request,pk):
    sel_point = Point.objects.get(pk=pk,point_institute= request.user.profile.institute)
    sel_point.status = "inactive"
    sel_point.save()
    messages.success(request, 'Point Deleted successfully !')  
    return HttpResponseRedirect(f'/bus/')



def fetch_bus_details(request):
    # pk=request.POST.get('category')
    selected_bus = Bus.objects.get(pk=request.POST.get('category'))
    if selected_bus.status == "active":
        selected_bus.status = "inactive"
        selected_bus.save()
    else:
        selected_bus.status = "active"
        selected_bus.save()
    return HttpResponse("Hello world")

def get_last_digits(num, last_digits_count=8):
    return abs(num) % (10**last_digits_count)

def first_n_digits(num, n=4):
    return num // 10 ** (int(math.log(num, 10)) - n + 1)

def add_driver(request):
    all_states = State.objects.all()
    context_data = {
        'all_states':all_states
    }
    return render(request, 'bus/driver.html', context_data)

def add_new_driver(request):
    if request.method == 'POST':
        last = Institute_levels.objects.filter(institute=request.user.profile.institute).first()
        print(last)
        l_id= int(last.level_id)+1
        try:
            chk_role = Institute_levels.objects.get(institute=request.user.profile.institute, level_name='driver')
            create_level = chk_role
        except Institute_levels.DoesNotExist:
            create_level = Institute_levels.objects.create(institute=request.user.profile.institute,level_id=l_id, level_name='driver')
            print("except")
        d_code = request.POST['driver_code'].strip()
        f_name = request.POST['first_name'].strip()
        m_name = request.POST['middle_name'].strip()
        l_name = request.POST['last_name'].strip()
        fat_name = request.POST['father_name'].strip()
        mot_name = request.POST['mother_name'].strip()
        gender = request.POST['gender'].strip()
        dob = request.POST['dob']
        marital_status = request.POST['marital_status']
        category = request.POST['category_']
        profile= request.FILES.get('pc')
        m_num = request.POST.get('mobile_number')
        email = request.POST['email'].strip()
        aadhar_card_number = request.POST['adhar_number']
        d_lic = request.POST['driving_license'].strip()
        add_one = request.POST['address_line_1'].strip()
        add_two = request.POST['address_line_2'].strip()
        city = request.POST['city'].strip()
        state = request.POST['state'].strip()
        sel_state = State.objects.get(pk=state)
        pin = request.POST['u_pin_code'].strip() 

        # creating user object
        pwd = get_last_digits(int(aadhar_card_number))
        start_digit = first_n_digits(int(aadhar_card_number))
        user_name = f_name+str(start_digit)
        driver_user = User.objects.create_user(user_name , email, pwd)
        driver_user.save()
        search_user = UserProfile.objects.get(user=driver_user)
        print(search_user)
        # creating Userprofile object
        search_user.institute= request.user.profile.institute
        search_user.designation=create_level
        search_user.first_name=f_name
        search_user.middle_name=m_name
        search_user.last_name=l_name
        search_user.father_name=fat_name
        search_user.mother_name=mot_name
        search_user.gender=gender
        search_user.date_of_birth=dob
        search_user.marital_status=marital_status
        search_user.category=category
        search_user.aadhar_card_number=aadhar_card_number
        search_user.profile_pic=profile
        search_user.mobile_number=m_num
        search_user.address_line_1=add_one
        search_user.address_line_2=add_two
        search_user.city=city
        search_user.state=sel_state
        search_user.pin_code=pin
        search_user.status="approve"
        search_user.save()

        # creating driver info object
        driver = Driver.objects.create(driver_id=d_code, name=search_user,driving_lic_no=d_lic, institute= search_user.institute)
        # creating role description object
        role_des = Role_Description.objects.create(user=driver_user, institute= request.user.profile.institute, level=create_level)
        messages.success(request, 'Driver added successfully !') 
        messages.info(request,f' Driver ID & Password is id:-{email}, password:-{pwd} ')
        return HttpResponseRedirect(f'/bus/')  

def add_route(request):
    if request.method == 'POST':
        r_no = request.POST['route_no'].strip()
        r_name = request.POST['route_name'].strip()
        r_bus = request.POST['sel_bus']
        sel_b = Bus.objects.get(pk=r_bus)
        r_driver = request.POST['sel_driver']
        sel_d = Driver.objects.get(pk=r_driver)
        r_from_date = request.POST['from_date']
        r_to_date = request.POST['to_date']
        print(r_from_date)
        print(r_to_date)
        
        new_route = RouteInfo.objects.create(route_no=r_no, route_name=r_name, vehicle=sel_b, vehicle_driver=sel_d,institute=request.user.profile.institute , from_date=r_from_date, to_date=r_to_date)
        messages.success(request, 'Route created successfully !') 

        return HttpResponseRedirect(f'/bus/')  

