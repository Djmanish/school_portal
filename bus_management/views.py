from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages
from django.utils import timezone
from notices.models import *
from datetime import datetime, timedelta

# Create your views here.
def bus(request):
    buses = Bus.objects.filter(bus_institute=request.user.profile.institute)
    states_list = State.objects.all()
    points = Point.objects.filter(point_institute=request.user.profile.institute)
    context_data = {
        'buses': buses,
        'states_list': states_list,
        'points':points,
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

def add_driver(request):
    driver_user = User.objects.create(username="manish", email="manish@example.com", password="test@1234")        
    return render(request, 'bus/driver.html')