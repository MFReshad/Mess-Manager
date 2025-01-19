from django.shortcuts import render , redirect

# Create your views here.

from .forms import CreateUserForm, LoginForm, AddRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from . models import Record

# from django.http import HttpResponse



# Homepage

def home(request):
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


#  login user

def mylogin(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('dashboard')

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

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST , instance=record)

        if form.is_valid():

            form.save()

            return redirect('dashboard')
        
    context = {'form' : form}

    return render(request, 'webapp/update-record.html', context=context)



# Read record

@login_required(login_url='my-login')
def read_record(request, pk):

    record = Record.objects.get(id=pk)
    
    context = {'record':record}

    return render(request, 'webapp/view-record.html', context= context)