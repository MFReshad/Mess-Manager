from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

from . models import Record , User , Bazar , Mess

# - Register/Create User

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']

# Testing create new user
class SignUp(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:

        model = User
        fields = ['first_name', 'last_name' ,'username', 'email'  ]
    

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return password_confirm

# Login User

class LoginForm(AuthenticationForm):

    username = forms.EmailField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



# Create Record

class AddRecordForm(forms.ModelForm):
 
    class Meta:

        model = Record
        fields = ['firstName', 'lastName', 'email', 'phone',  'address', 'city', 'province', 'country']


# Update Record

class UpdateRecordForm(forms.ModelForm):
 
    class Meta:

        model = Record
        fields = ['firstName', 'lastName', 'email', 'phone', 'address', 'city', 'province', 'country']



# ###### Bazar ######

# add bazar

class AddBazarItem(forms.ModelForm):

    class Meta:

        model = Bazar
        fields = [ 'item_name', 'quantity', 'price', 'unit', 'done_by' ]

        widgets = {
            'item_name': forms.TextInput(attrs={'class': "form-control"}), 
            'quantity' :forms.TextInput(attrs={'class': "form-control"}),  
            'price': forms.TextInput(attrs={'class': "form-control"}), 
            'unit': forms.Select(attrs={'class': "form-select"}), 
            'done_by': forms.Select(attrs={'class': "form-select"})
            
        }
    
    def __init__(self, *args, **kwargs ):
    
        request = kwargs.pop('request' , None)
        super().__init__(*args, **kwargs)

        if request:
            mess = request.user.in_mess
            self.fields['done_by'].queryset = mess.user.all()