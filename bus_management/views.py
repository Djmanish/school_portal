from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from main_app.models import*
from .models import *
from django.contrib import messages
from django.utils import timezone
from notices.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from bus_management import vehicle_signals
import math

# Create your views here.
def bus(request):
    buses = Bus.objects.filter(bus_institute=request.user.profile.institute)
    states_list = State.objects.all()
    points = Point.objects.filter(point_institute=request.user.profile.institute)
    drivers = Driver.objects.filter(institute=request.user.profile.institute)
    active_buses = Bus.objects.filter(bus_institute=request.user.profile.institute, status="active")
    routes = RouteInfo.objects.filter(institute=request.user.profile.institute, status="active")
    new = RouteInfo.objects.filter(institute=request.user.profile.institute)
    for i in new:
        i.point_count= RouteMap.objects.filter(route=i).count()
        s= RouteMap.objects.filter(route=i, index=0+1)
        for j in s:
            i.st= j.time
        l= RouteMap.objects.filter(route=i, index=i.point_count)
        for k in l:
            i.lt= k.time
       
    context_data = {
        'buses': buses,
        'states_list': states_list,
        'points':points,
        'drivers':drivers,
        'active_buses':active_buses,
        'routes':routes,
        'new':new,
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
            messages.error(request, 'Vehicle with this registration number already exists !')
            return HttpResponseRedirect(f'/bus/')    
        except Bus.DoesNotExist:
            new_bus = Bus.objects.create(bus_no=b_no, bus_maker=b_maker, vehicle_type=b_type,fuel_type=b_fuel, bus_color=b_color, bus_capacity=b_capacity, bus_institute=request.user.profile.institute)
            messages.success(request, 'Vehicle added successfully !')  
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
        messages.success(request, 'Vehicle details updated successfully !')  
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
        p_country = request.POST['point_country'].strip()
        p_long = request.POST['point_longitute']
        p_lat = request.POST['point_latitute']
        if p_street_no == "":
            p_street_no = None
        
        try:
            chk_point= Point.objects.get(point_code=p_code, point_institute=request.user.profile.institute)
        except Point.DoesNotExist:
            chk_point = 0 
        if chk_point == 0:
            new_point = Point.objects.create(point_code=p_code, point_name=p_name, point_street_no=p_street_no, point_landmark=p_landmark,point_exact_place=p_place, point_city=p_city, point_state=sel_state, point_country=p_country,  point_institute=request.user.profile.institute, longitude=p_long ,latitude=p_lat)
            messages.success(request, 'Point added successfully !')  
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
        point.longitude = request.POST['edit_point_longitute']
        point.latitude = request.POST['edit_point_latitute']
        point.save()
        messages.success(request, 'Point details updated successfully !')  
        return HttpResponseRedirect(f'/bus/') 

def edit_route(request):
    if request.method == 'POST':
        selected_route = request.POST['edit_route_id_hide']
        r = RouteInfo.objects.get(pk=selected_route)
        r_bus = request.POST['edit_sel_bus']
        bus = Bus.objects.get(pk=r_bus)
        r_driver = request.POST['edit_sel_driver']
        driver = Driver.objects.get(pk=r_driver)
        r.route_no= request.POST['edit_route_no']
        r.route_name = request.POST['edit_route_name']
        r.vehicle = bus
        r.vehicle_driver = driver
        r.from_date = request.POST['edit_from_date']
        r.to_date = request.POST['edit_to_date']
        r.save()
        messages.success(request, 'Route info updated successfully !')  
        return HttpResponseRedirect(f'/bus/')


def delete_route(request,pk):
    sel_route = RouteInfo.objects.get(pk=pk,institute= request.user.profile.institute)
    sel_route.status = "inactive"
    sel_route.save()
    r = RouteMap.objects.filter(route=sel_route)
    for i in r:
        i.delete()
    messages.success(request, 'Route deleted successfully !')  
    return HttpResponseRedirect(f'/bus/')

def delete_point(request,pk):
    sel_point = Point.objects.get(pk=pk,point_institute= request.user.profile.institute)
    sel_point.status = "inactive"
    sel_point.save()
    messages.success(request, 'Point deleted successfully !')  
    return HttpResponseRedirect(f'/bus/')

def delete_routemap(request,pk):
    sel_route = RouteInfo.objects.get(pk=pk)
    s= RouteMap.objects.filter(route=sel_route)
    for i in s:
        i.delete()
    
    messages.success(request, 'Route map deleted successfully !')  
   
    return HttpResponseRedirect(f'/bus/')

def delete_view_routepoints(request,pk):
    del_point = Point.objects.get(pk=pk)
    ss= RouteMap.objects.filter(point=del_point)
    for i in ss:
        i.delete()
    
    messages.success(request, 'Point deleted successfully !')  
   
    return HttpResponseRedirect(f'/bus/')

# def edit_view_routepoints(request,pk):
    



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
        messages.info(request,f' Driver email & password are id: {email}, password: {pwd} ')
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
        
        new_route = RouteInfo.objects.create(route_no=r_no, route_name=r_name, vehicle=sel_b, vehicle_driver=sel_d,institute=request.user.profile.institute , from_date=r_from_date, to_date=r_to_date)
        messages.success(request, 'Route created successfully !') 

        return HttpResponseRedirect(f'/bus/')  

def route_map(request):
    if request.method == 'POST':
        route = int(request.POST['route'])
        point = int(request.POST['point'])
        sch_route = RouteInfo.objects.get(id=route)
        points = Point.objects.filter(point_institute=request.user.profile.institute)
        context_data = {
        'sch_route':sch_route,
        'range':range(point),
        'points':points,
        
        }
    
        return render(request, 'bus/map_route.html', context_data)  

def update_map_route(request):
    if request.method == 'POST':
        r_id = int(request.POST['point_code_hidden'])
        r_routes = RouteInfo.objects.get(id=r_id)
        point = int(request.POST['update_map_point'])
        
        points = Point.objects.filter(point_institute=request.user.profile.institute)
        context_data = {
        'range':range(point),
        'points':points,
        'r_routes':r_routes,
        }
        
        return render(request, 'bus/update_map_route.html', context_data)  

def update_route(request):
    if request.method == 'POST':
        select_point= request.POST.getlist('select_point')
        select_time= request.POST.getlist('select_time')
        route= int(request.POST['hide_route'])
        select_index= request.POST.getlist('index')
       
        result= checkIfDuplicates_1(select_point)
        if result:
            messages.error(request, "You are selecting same point !")  
                      
            return HttpResponseRedirect(f'/bus/') 
        else:
            print ("non Duplicates")

        result1= checkIfDuplicates_1(select_time)
        if result1:
            messages.error(request, "Time never be same !")  
                      
            return HttpResponseRedirect(f'/bus/') 
        else:
            print ("non Duplicates")   

        result2= checkIfDuplicates_1(select_index)
        if result2:
            messages.error(request, "Index number never be same !")  
                      
            return HttpResponseRedirect(f'/bus/') 
        else:
            print ("non Duplicates")      
        length=len(select_point) 
        for i in range(length):
            s_point= Point.objects.get(id=select_point[i])
            ind= select_index[i]
            try:
                sch_r= RouteMap.objects.get(route__id=route, index=ind)
                q= RouteMap.objects.filter(route__id=route)
                for k in q:
                    if int(k.index) >= int(ind):
                        a= RouteMap.objects.get(route__id=route, index=k.index)
                        a.index= int(k.index+1)
                        a.save()
                       
                new= RouteMap.objects.create(route=sch_r.route, point=s_point, index=ind, time=select_time[i], routemap_institute= request.user.profile.institute)        
                print(sch_r)
                
            except RouteMap.DoesNotExist:
                sch_r= RouteMap.objects.filter(route__id=route).last()
                inr= sch_r.index
                print(inr)
                new= RouteMap.objects.create(route=sch_r.route, point=s_point, index=inr+1, time=select_time[i], routemap_institute= request.user.profile.institute)
        messages.success(request, "Route map created successfully !")     
    return HttpResponseRedirect(f'/bus/')
    # return HttpResponse('hello')
       

def checkIfDuplicates_1(listOfElems):
    # ''' Check if given list contains any duplicates '''
    if len(listOfElems) == len(set(listOfElems)):
      return False
    else:
      return True

def add_point_route (request):
    if request.method == 'POST':
        select_point= request.POST.getlist('select_point')
        select_time= request.POST.getlist('time')
        route= int(request.POST['hide_route'])
        s_route= RouteInfo.objects.get(id=route)
        result= checkIfDuplicates_1(select_point)
        if result:
            messages.error(request, "You are selecting same point !")  
                      
            return HttpResponseRedirect(f'/bus/') 
        else:
            print ("non Duplicates")

        result1= checkIfDuplicates_1(select_time)
        if result1:
            messages.error(request, "Time never be same !")  
                      
            return HttpResponseRedirect(f'/bus/') 
        else:
            print ("non Duplicates")   
        length=len(select_point) 
        for i in range(length):
            s_point= Point.objects.get(id=select_point[i])
            new= RouteMap.objects.create(route=s_route, point=s_point, index=i+1, time=select_time[i], routemap_institute= request.user.profile.institute)
        messages.success(request, "Point(s) added successfully !")     
    return HttpResponseRedirect(f'/bus/') 
    
def set_location(request):
    if request.method == 'POST':
        longi = request.POST['longitute'].strip()
        lati = request.POST['latitute'].strip()
        print(longi)
        print(request.user.profile.institute.id)
        try:
            sch = InstituteLocation.objects.get(institute=request.user.profile.institute)
        except InstituteLocation.DoesNotExist:
            sch = 0
            set_loc = InstituteLocation.objects.create(institute=request.user.profile.institute, longitute=longi, latitude = lati)
            messages.success(request, 'Institute location updated successfully !')
            return HttpResponseRedirect(f'/bus/')
    if sch:
        sch.longitute = longi
        sch.latitude = lati
        sch.save()
        messages.success(request, 'Institute location updated successfully !')
        return HttpResponseRedirect(f'/bus/')

def see_map(request):
    ins_loc = InstituteLocation.objects.get(institute=request.user.profile.institute)

    context_data={
    'ins_loc':ins_loc,
    }
    return render(request, 'bus/index.html', context_data)

       
    
def start_trip(request):
    u = RouteInfo.objects.get(vehicle_driver__name=request.user.profile)
    sel_r = u.id
    p = RouteMap.objects.filter(route__id=sel_r)
    vehicle_signals.start.send(sender=None,route=u)
    context={
        'p':p,
    }
    return render(request, 'bus/trip.html', context)

def add_trip(request):
    if request.method == 'POST':
        ids = int(request.POST['route_id'])
        date =datetime.now().date()
        print(date)
        r_map = RouteMap.objects.get(id=ids)
        route = r_map.route
        point = r_map.point
        driver = r_map.route.vehicle_driver
        try:
            sch_data = Trip.objects.get(route = route, point = point, driver=driver, date = date)
            return HttpResponse('<h6 style="color: red;">Already Entered</h6>')
        except Trip.DoesNotExist:
            new = Trip.objects.create(route=route, point= point, driver=driver, time=datetime.now().strftime('%H:%M:%S') ,date= date)
            return HttpResponse('<h6 style="color: green;">Submitted</h6>')
        
        
def view_routepoints(request, pk):
    # view_point = Point.objects.get(pk=pk)
    view_route = RouteInfo.objects.get(pk=pk)
    maps = RouteMap.objects.filter(route=view_route)
   
    context_data = {
    'view_route': view_route,
    'maps': maps,
    }
    
    return render(request, 'bus/view_routepoints.html', context_data)

def update_routepoints(request):
    
    if request.method == 'POST':
        route_point = request.POST['edit_routepoint_id_hide']
        p = RouteMap.objects.get(id= route_point)
        p_index= request.POST['edit_routeindex']
        p_time = request.POST['edit_routetime']

        p.index = p_index
        p.time = p_time
                
        p.save()
        
        # context_data = {
        # 'route_editpoint' : route_editpoint,
        # }
        messages.success(request, 'Point Details Updated successfully !') 
        return HttpResponseRedirect(f'/bus/')
      
    
    
    