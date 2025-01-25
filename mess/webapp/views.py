from django.shortcuts import render , redirect , get_object_or_404

# Create your views here.

from .forms import CreateUserForm, LoginForm, AddRecordForm, UpdateRecordForm , SignUp , AddBazarItem

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from . models import Record, Mess, Bazar

from django.http import HttpResponse

from django.contrib import messages

from django.db import models
from django.db.models import Sum,  F, Value
from django.db.models.functions import Concat ,Coalesce


from datetime import datetime

# from mess.webapp import models


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

    form = LoginForm()

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
                        return redirect('dashboard')
                    # print("User in group.")
                else:
                    return redirect('create_mess')
                    # print("User in not group.")
            

    context = {'form':form}

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

@login_required
def create_mess(request):

    if request.user.in_mess:  # If user already belongs to a group
        return HttpResponse("you are in a mess")
    
    if request.method == 'POST':
        mess_name = request.POST['mess_name']
        # Create a new group
        new_mess = Mess.objects.create(name=mess_name)
        
        # Assign the user to the newly created group
        request.user.in_mess = new_mess
        request.user.save()
         
        return redirect('dashboard')

    return render(request, 'webapp/create_mess.html')


####### Bazar #######

# Bazar list group by date
@login_required(login_url='my-login')
def bazar_list(request):

    member = request.user
    member_of_mess = member.in_mess

    if not member_of_mess:
        return redirect('join-mess')

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
            total_price=Sum('price'),  # Total price for each date
        )
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
def bazar_list_date(request , date):

    member = request.user
    member_of_mess = member.in_mess

    if not member_of_mess:
        return redirect('join-mess')


    # Convert the string date to a date object
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        # If the date format is incorrect, handle the error
        return redirect('bazar-list')  # Or show an error message

    # Filter records by the selected date
    all_records = Bazar.objects.filter(mess=member_of_mess, date=date_obj)
    total_price = all_records.aggregate(total_price=Sum('price'))['total_price']

  
    context = {
        'items': all_records,
        'date': date_obj,
        'total_price': total_price,
    }

    return render(request, 'webapp/bazar-list-details-date.html', context=context)




# add bazar item

def add_bazar(request , mess_name_slug ):
    
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
            return redirect('bazar-list')
    else:
        form = AddBazarItem(request=request)
    
    return render(request, 'webapp/add_bazar_item.html', {'form': form, 'mess': mess})


