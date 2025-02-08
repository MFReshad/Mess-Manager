from django.shortcuts import render , redirect , get_object_or_404

# Create your views here.

from .forms import CreateUserForm, LoginForm, AddRecordForm, UpdateRecordForm , SignUp , AddBazarItem

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from . models import Record, Mess, Bazar, User , MealSchedule , NextDayMeal , Meal

from django.http import HttpResponse

from django.contrib import messages

from django.db import models
from django.db.models import Sum,  F, Value
from django.db.models.functions import Concat ,Coalesce

from django.core.exceptions import ObjectDoesNotExist


from datetime import datetime , timedelta

# from mess.webapp import models
from django.views.decorators.cache import never_cache

from . tasks import sleeptime , test_func

from collections import defaultdict


# Homepage

def home(request):
    if not request.user.is_anonymous:
        # print(request.user)
        return redirect('dashboard')
    # return HttpResponse("Hello World")
    return render(request, 'webapp/index.html' )

# Register

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('my-login')
    
    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)

# Register Test

def register_user_mess(request):

    form = SignUp()

    if request.method == "POST":

        form = SignUp(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            # form.save()

            # return HttpResponse("Hello World")
            return redirect('my-login')
    
    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)


#  login user

def mylogin(request):

    next_url = request.GET.get('next', 'dashboard')
    form = LoginForm()

    if not request.user.is_anonymous:
        return redirect('dashboard')
    
    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            email = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                # print("Authentication  user.")
                auth.login(request, user)

                if user.in_mess:
                    if user.is_admin:
                        # print("You are admin")
                        # return redirect('dashboard')
                        return HttpResponse('Admin Dashboard is on working')
                    else:
                        # print("You are not admin")
                        return redirect(next_url)
                    # print("User in group.")
                else:
                    return redirect('create_mess')
                    # print("User in not group.")
            

    context = {'form':form, 'next': next_url}

    return render(request, 'webapp/login.html', context=context)



# Logout

def user_logout(request):

    auth.logout(request)

    return redirect('my-login')




# Dashboard
@login_required(login_url='my-login')
def dashboard(request):

    all_records = Record.objects.all()
   
    context = {'records': all_records}

    return render(request, 'webapp/dashboard.html', context=context )


# Add record / Create record

@login_required(login_url='my-login')
def create_record(request):
    
    form = AddRecordForm()

    if request.method == "POST":

        form = AddRecordForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('dashboard')
    
    context = {'form':form}

    return render(request, 'webapp/create-record.html', context=context)



# Update record

@login_required(login_url='my-login')
def update_record(request, pk):

    # record = Record.objects.get(id=pk)
    record = get_object_or_404(Record, id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST , instance=record)

        if form.is_valid():

            form.save()

            return redirect('dashboard')
        
    context = {'form' : form}

    return render(request, 'webapp/update-record.html', context=context)



# Read a single record

@login_required(login_url='my-login')
def read_record(request, pk):

    record = Record.objects.get(id=pk)
    
    context = {'record':record}

    return render(request, 'webapp/view-record.html', context= context)

# Delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)
    
    record.delete()
    
    messages.info(request, f'Record {pk} delete succesfully!')

    return redirect('dashboard')

    # context = {'record':record}

    # return render(request, 'webapp/view-record.html', context= context)


# ####### MESS #######

# Create Mess

@login_required(login_url='my-login')
def create_mess(request):

    if request.user.in_mess:  # If user already belongs to a group
        # return HttpResponse("you are in a mess")
        return redirect('dashboard')
    
    if request.method == 'POST':
        mess_name = request.POST['mess_name']
        # Create a new group
        new_mess = Mess.objects.create(name=mess_name)
        
        # Assign the user to the newly created group
        request.user.in_mess = new_mess
        request.user.is_admin = True
        request.user.save()
         
        return redirect('dashboard')

    return render(request, 'webapp/create_mess.html')

# Join Mess

@login_required(login_url='my-login')
def join_mess(request):

    if request.user.in_mess:  # If user already belongs to a group
        # return HttpResponse("you are in a mess")
        return redirect('dashboard')
    
    if request.method == 'POST':
        mess_code = request.POST.get('mess_code', '').strip()
        
        try:
            find_mess = Mess.objects.get(mess_code = mess_code)
            
            # Assign the user to the newly created group
            request.user.in_mess = find_mess
            request.user.save()
            messages.info(request, f'Welcome to {request.user.in_mess.name}')
            return redirect('dashboard')
        
        except ObjectDoesNotExist:
            messages.info(request, f'No Mess Found!!')
            return redirect('join_mess')
        

    return render(request, 'webapp/join-mess.html')


# view mess of info

@login_required(login_url='my-login')
@never_cache
def my_mess(request):

    if request.user.in_mess:

        mess_info = Mess.objects.get(name = request.user.in_mess.name)

        context = {'mess': mess_info}

        if request.POST:
            lunch_time = request.POST.get('appt')
            meal_time = request.POST.get('appt2')
            
            Mess.objects.update(name = request.user.in_mess.name , lunch_update_time = lunch_time, meal_update_time = meal_time)

            return redirect(request.path)
        
    else:
        return redirect('join_mess')

    return render(request, 'webapp/mess.html' , context= context)


# Leave Mess
@login_required(login_url='my-login')
@never_cache
def leave_mess(request):

    if request.user.in_mess:

        request.user.in_mess = None
        request.user.save()
        
        return redirect('join_mess')
    


####### Bazar #######

# Bazar list group by date
@login_required(login_url='my-login')
@never_cache
def bazar_list(request):

    member = request.user
    member_of_mess = member.in_mess

    if not member_of_mess:
        return redirect('join_mess')

    # Default to the current month and year
    current_date = datetime.now()
    selected_month = request.GET.get('month', current_date.strftime('%Y-%m'))

    # Parse the selected month and year
    try:
        year, month = map(int, selected_month.split('-'))
    except ValueError:
        year, month = current_date.year, current_date.month


    # Filter records by the selected month and year
    all_records = Bazar.objects.filter(
        mess=member_of_mess,
        date__year=year,
        date__month=month
    )
  
    # Group records by date and calculate total price
    grouped_records = (
        Bazar.objects.filter(mess=member_of_mess, date__year=year, date__month=month)
        .values('date')  # Group by date
        .annotate(
            total_price=Sum('price'))  # Total price for each date
        .order_by('-date')
    )

    # Collect items per date
    items_per_date = {}
    for bazar in Bazar.objects.filter(mess=member_of_mess, date__year=year, date__month=month):
        date_key = bazar.date.strftime('%Y-%m-%d')
        if date_key not in items_per_date:
            items_per_date[date_key] = []
        items_per_date[date_key].append(bazar.item_name)

    # Merge grouped records with items
    for record in grouped_records:
        record['items'] = ', '.join(items_per_date.get(record['date'].strftime('%Y-%m-%d'), []))

    # print("Grouped Records:", grouped_records)  # Debugging

    context = {
        # 'items': grouped_records,
        'grouped_records': grouped_records,
        'selected_month': selected_month,  # Pass the selected month to the template
    }

    return render(request, 'webapp/bazar-list.html', context=context)



# Bazar list detail by date
@login_required(login_url='my-login')
@never_cache
def bazar_list_date(request , date):

    member = request.user
    member_of_mess = member.in_mess

    if not member_of_mess:
        return redirect('join_mess')


    # Convert the string date to a date object
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        # If the date format is incorrect, handle the error
        return redirect('bazar-list')  # Or show an error message

    # Filter records by the selected date
    all_records = Bazar.objects.filter(mess=member_of_mess, date=date_obj)
    total_price = round(all_records.aggregate(total_price=Sum('price'))['total_price'], 2)
    # round(n, 2)
  
    context = {
        'items': all_records,
        'date': date_obj,
        'total_price': total_price,
    }

    return render(request, 'webapp/bazar-list-details-date.html', context=context)




# add bazar item
@login_required(login_url='my-login')
def add_bazar(request , mess_name_slug ):
    
    if request.user.in_mess:
        if request.user.is_admin:

            mess = get_object_or_404(Mess, id=request.user.in_mess.id)

            # print(mess)
            mess_name_slug = mess.name.replace(" ", "-")

            if request.method == 'POST':
                form = AddBazarItem(request.POST , request=request)  ##why
                if form.is_valid():
                    # form.save()
                    bazar_item = form.save(commit=False)  # Don't save to the database yet
                    bazar_item.mess = mess  # Set the mess explicitly
                    bazar_item.save()

                    if request.POST.get('action') == 'add_more':
                        return redirect('add_bazar_list', request.user.in_mess)
                    else:
                        return redirect('bazar-list')
            else:
                form = AddBazarItem(request=request)
        else:
            return redirect('bazar-list')
    else:
        return redirect('join_mess')
    
    return render(request, 'webapp/add_bazar_item.html', {'form': form, 'mess': mess})


# view mess of info
# not complete
@login_required
@never_cache
def user_dashboard(request):

    user = request.user

    if request.user.in_mess:

        user_info = User.objects.get(username = request.user.username)

            # Default to the current month and year
        current_date = datetime.now()
        # print(current_date)
        selected_month =  current_date.strftime('%Y-%m')

        # Parse the selected month and year
        try:
            year, month = map(int, selected_month.split('-'))
        except ValueError:
            year, month = current_date.year, current_date.month

            # Convert the string date to a date object
    try:
        date_obj = datetime.strptime(selected_month, '%Y-%m').date()
        # print(date_obj)
    except ValueError:
        # If the date format is incorrect, handle the error
        return redirect('bazar-list')  # Or show an error message

    # Filter records by the selected date
    all_records = Bazar.objects.filter(mess=request.user.in_mess, date__year=year, date__month=month)
    # total_month_cost_of_bazar = round(all_records.aggregate(total_price=Sum('price'))['total_price'] , 2)
    # total_month_cost_of_bazar = round(all_records.aggregate(total_price=Sum('price')).get('total_price', 0), 2)
    total_price = all_records.aggregate(total_price=Sum('price'))['total_price']

# If total_price is None, default to 0.00
    total_month_cost_of_bazar = round(total_price if total_price is not None else 0.00 , 2)

    all_meals = Meal.objects.filter(mess=request.user.in_mess, date__year=year, date__month=month)

    total_meal = all_meals.aggregate(total_meal=Sum('total_meal'))['total_meal']
    # print(all_records)
    # print(total_month_cost_of_bazar)
    # round(n, 2)
    all_users_meal_totals = defaultdict(lambda: {'lunch': 0, 'dinner': 0, 'total': 0})

    for meal in all_meals:
        user = meal.user.username
        all_users_meal_totals[user]['lunch'] += meal.lunch
        all_users_meal_totals[user]['dinner'] += meal.dinner
        all_users_meal_totals[user]['total'] += meal.lunch + meal.dinner

    mealrate = total_month_cost_of_bazar / total_meal
    meal_rate = round(mealrate if mealrate is not None else 0.00 , 2)

    user_total_meal = sum(meal.total_meal for meal in all_meals.filter(user = user))
    user_meal_cost = meal_rate * user_total_meal

    context = {'user': user_info, 'total_meal_cost' : total_month_cost_of_bazar, 'total_meal': total_meal, 'meal_rate': meal_rate, 'user_total_meal' : user_total_meal, 'user_meal_cost':user_meal_cost}

    return render(request, 'webapp/dashboard-user.html' , context= context)


@login_required
@never_cache
def meal_schedule(request):
    user = request.user
    days_of_week = ["sat", "sun", "mon", "tue", "wed", "thu", "fri"]

    formatted_lunch_time = user.in_mess.lunch_update_time.strftime("%H:%M").lstrip("0")
    formatted_meal_time = user.in_mess.meal_update_time.strftime("%H:%M").lstrip("0")

    today = datetime.now() 
    time = Mess.objects.filter(name = user.in_mess.name).first()
    # print(f'got from db - {time}')
    lunch_editable = None

    if time:
        lunch_hour = time.lunch_update_time.hour
        # print(lunch_hour)
        meal_hour = time.meal_update_time.hour

        if today.hour >= meal_hour:
            today = datetime.now() + timedelta(1)

        
        if today.hour <= lunch_hour or today.hour >= meal_hour:
                lunch_editable = True 
        
        #         print(f'get lunch')
        # print(today)

    # print(f'this is today - {today}')
    formating = datetime.strftime(today, "%A, %d-%b-%Y")
    today_week = datetime.strftime(today, "%a").lower()

    lunch_, dinner_ = 0, 0
    

    if user.in_mess:
        next_meal =  NextDayMeal.objects.filter(user=user).first()
        

        if next_meal:
            print('next meal')
            showdate = next_meal.day
            formating = datetime.strftime(showdate, "%A, %d-%b-%Y")
            lunch_ = next_meal.lunch
            dinner_ = next_meal.dinner

            
                # print(lunch_editable)


        else:
            meal_today = MealSchedule.objects.filter(user=user,day=today_week).first()

            if meal_today:
                lunch_ = meal_today.lunch
                dinner_ = meal_today.dinner

                NextDayMeal.objects.update_or_create(
                        user=user,
                        defaults={
                            'day' : today,
                            'lunch' : lunch_, 
                            'dinner': dinner_
                        }
                    )
            # else:
            #     MealSchedule.objects.create(user=user)
            
        
        if request.method == "POST" and 'btnform2' in request.POST:
            if lunch_editable:
                lunch_value = int(request.POST.get(f"_lunch_"))
            else:
                lunch_value = lunch_
            dinner_value = int(request.POST.get(f"_dinner_"))
            NextDayMeal.objects.update_or_create(
                user=user,
                defaults=  {
                    'lunch': lunch_value, 
                    'dinner':dinner_value
                    }
            )
            # print(lunch_value)
            # print(dinner_value)
            # print('Button 2')
            return redirect(request.path)
    

    if request.method == "POST" and 'btnform1' in request.POST:
        for day in days_of_week:
            lunch_value = int(request.POST.get(f"lunch_{day}", 0))
            dinner_value = int(request.POST.get(f"dinner_{day}", 0))

            # Update or create the meal schedule for the user
            MealSchedule.objects.update_or_create(
                user=user,
                day=day,
                defaults={"lunch": lunch_value, "dinner": dinner_value}
            )
        return redirect(request.path)

    # Ensure all days exist with initial values (lunch=0, dinner=0)
    if lunch_editable:
        for day in days_of_week:
            MealSchedule.objects.get_or_create(user=user, day=day, defaults={"lunch": 1, "dinner": 1})
    else:
        for day in days_of_week:
            MealSchedule.objects.get_or_create(user=user, day=day, defaults={"lunch": 0, "dinner": 1})
    # Fetch user's meals in correct order
    meals = MealSchedule.objects.filter(user=user).order_by(
        models.Case(
            models.When(day="sat", then=1),
            models.When(day="sun", then=2),
            models.When(day="mon", then=3),
            models.When(day="tue", then=4),
            models.When(day="wed", then=5),
            models.When(day="thu", then=6),
            models.When(day="fri", then=7),
            default=8
        )
    )
    # print(formating)
    # print(lunch_editable)
    # print(lunch_)
    # print(dinner_)
    # print(formatted_lunch_time)
    # print(formatted_meal_time)

    context = {"meals": meals, "date":formating ,'edit_lunch' : lunch_editable, 'lunch':lunch_ , 'dinner':dinner_,  'tlunch' : formatted_lunch_time, 'tmeal' : formatted_meal_time}

    return render(request, "webapp/meal_schedule.html", context=context )




@login_required(login_url='my-login')
@never_cache
def meal_(request):
    if request.user.in_mess:
        current_date = datetime.now()
        selected_month = request.GET.get('month', current_date.strftime('%Y-%m'))
        selected_user = request.GET.get('user', '')

        try:
            year, month = map(int, selected_month.split('-'))
        except ValueError:
            year, month = current_date.year, current_date.month

        users_in_mess = User.objects.filter(in_mess=request.user.in_mess)

        all_meals = Meal.objects.filter(mess=request.user.in_mess, date__year=year, date__month=month)

        if selected_user and selected_user != "all":
            
            all_meals = all_meals.filter(user__username=selected_user)

        if request.method == "POST":
            username = request.POST.get("user")  
            date = request.POST.get("date")  
            lunch = request.POST.get("lunch")
            dinner = request.POST.get("dinner")
            # Meal.objects.update(user__username = username, date= date, lunch = lunch, dinner = dinner) #WRONG
            try:

                date_obj = datetime.strptime(date, '%b. %d, %Y').date()
                # Find the User object by username
                user = User.objects.get(username=username)
                
                # Retrieve the meal entry for this user and date
                meal = Meal.objects.get(user=user, date=date_obj)
                
                # Update the values
                meal.lunch = lunch
                meal.dinner = dinner
                
                
                # Save the updated meal object
                meal.save()

            except Meal.DoesNotExist:
                pass
            

            return redirect(request.path)
        # print(all_meals)
        # user_meal_totals = defaultdict(lambda: {'lunch': 0, 'dinner': 0, 'total': 0 , 'date':None})

        # for meal in all_meals:
        #     user = meal.user.username  # or meal.user.id if needed
        #     user_meal_totals[user]['lunch'] += meal.lunch
        #     user_meal_totals[user]['dinner'] += meal.dinner
        #     user_meal_totals[user]['total'] += meal.total_meal
        #     user_meal_totals[user]['date'] += meal.date


        # Convert defaultdict to a normal dictionary if needed
        # user_meal_totals = dict(user_meal_totals)

        context = {
            # "user_meal_totals" : dict(user_meal_totals),
            'user_meal_totals' : all_meals,
            'selected_month': selected_month,
            'selected_user': selected_user,
            'users_in_mess': users_in_mess,
        }
    else:
        return redirect('join_mess')

    return render(request, 'webapp/meal.html' , context=context)





def todays_meal_enter(request):
    
    # Retrieve mess_name from session if exists
    name = request.session.get("mess_name", None)
    # mess = request.session.get("mess", None)
    # name = mess.name
    # name = None
    if not name:
        if request.method == "POST":
            messcode = request.POST.get("mess_code")  

            try:

                lunch_editable = None

                mess = Mess.objects.get(mess_code = messcode)
                name = mess.name

                # Save mess_name in session
                request.session["mess_name"] = name  
                # request.session["mess"] = mess  

                return redirect('todays_meal')
    
            
            except ObjectDoesNotExist:
                messages.info(request, f'No Mess Found!!')
                return redirect('todays_meal_login')
            
    else:
        return redirect('todays_meal')
    #     print("WOrld")
        # request.session.pop("mess_name", None)
    
    # context = {
    #                 'mess_name' : name,
    #                 'meals' : meal,
    #                 'lunch' : lunch,
    #                 'dinner' : dinner,
    #                 'date' : formating,
    #                 'showLunch' : lunch_editable,
    #             }

            
    return render(request, 'webapp/todays-meal-login.html')


def todays_meal(request):

    name = request.session.get("mess_name", None)
    
    if name:
        mess = Mess.objects.get(name = name)
        meal = NextDayMeal.objects.filter(mess = mess)
        lunch_editable = None

        lunch, dinner = 0, 0
        # print("HELLO")
        lunch = meal.aggregate(lunch = Sum('lunch'))['lunch']
        # print(lunch)
        dinner = meal.aggregate(dinner = Sum('dinner'))['dinner']

        today = datetime.now()

        if today.time() >= mess.meal_update_time:
            today = datetime.now() + timedelta(1)
        
        if today.time() <= mess.lunch_update_time or today.time() >= mess.meal_update_time:
            lunch_editable = True
        
        formating = datetime.strftime(today, "%A, %d-%b-%Y")
    
    else:
        return redirect('todays_meal_login')
        
    context = {
            'mess_name' : name,
            'meals' : meal,
            'lunch' : lunch,
            'dinner' : dinner,
            'date' : formating,
            'showLunch' : lunch_editable,
        }

    return render(request, 'webapp/todays-meal.html' , context=context)
    


def test(request):
    # sleeptime(5)
    test_func.delay()
    return HttpResponse('Done Task')
    