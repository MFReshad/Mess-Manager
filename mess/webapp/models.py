from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


import secrets
import random
import string

# Create your models here.


class Mess(models.Model):
    name = models.CharField(max_length=100)
    mess_code = models.CharField(max_length=8, unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.mess_code:  
            self.mess_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_code():
        while True:
            code = ''.join(secrets.choice(string.ascii_letters + string.digits + '@#$') for _ in range(8))
            if not Mess.objects.filter(mess_code=code).exists():
                return code

    def __str__(self):
        return self.name





class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):

        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user

class User(AbstractBaseUser):

    # RESTAURANT = 1
    # CUSTOMER = 2

    # ROLE_CHOICE = (
    #     (RESTAURANT, 'Restaurant'),
    #     (CUSTOMER, 'Customer'),
    # )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100 , unique=True)
    phone = models.CharField(max_length=15, blank=True, unique=False, null=True)
    # role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required firelds
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_login = models.DateTimeField(auto_now_add=True)
    modified_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    in_mess = models.ForeignKey(
        Mess,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True




class Record(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)

    firstName = models.CharField(max_length=100)

    lastName = models.CharField(max_length=100)

    email = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    address = models.CharField(max_length=300)

    city = models.CharField(max_length=255)

    province = models.CharField(max_length=255)

    country = models.CharField(max_length=125)


    def __str__(self):
        return self.firstName + " " + self.lastName

    class Meta:
        ordering = ['-creation_date']




class Bazar(models.Model):

    KILOGRAM = 'kg'
    LITTER = 'L'

    UNIT_CHOICE = (
        (KILOGRAM, 'kg'),
        (LITTER, 'L')
    )

    date = models.DateField(auto_now_add=True)

    item_name = models.CharField(max_length=100)

    quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    unit = models.CharField(choices=UNIT_CHOICE,max_length=5, blank=True, null=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    mess = models.ForeignKey(
        Mess,
        on_delete=models.SET_NULL,
        null=True,  # if Mess is deleted it will be NuLL
        related_name='bazar'
    )

    done_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bazar'
    )

    def __str__(self):
        return self.item_name

    class Meta:
        ordering = ['-date']









