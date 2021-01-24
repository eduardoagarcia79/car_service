from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator_new(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First  name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address"
        email_check = self.filter(email_address=postData['email'])
        if email_check:
            errors['email'] = 'Email already in use. Please login'		
        if len(postData['email']) < 2:
            errors['email'] = "Email should be at least 2 characters"
        if len(postData['phone']) < 2:
            errors['phone'] = "Phone number should be at least 2 characters"
        return errors
    def basic_validator_login(self, postData):
        errors = {}
        if len(postData['email']) < 2:
            errors["email"] = "Email should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email_address=postData['email'])
        if not email_check:
            errors['email'] = 'Email does not exist'		
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        return errors
    def basic_validator_pwd(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if len(postData['conf_password']) < 8:
            errors["conf_password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['conf_password']:
            errors["conf_password"] = "Passwords doesn't match"
        return errors

class ServiceManager(models.Manager):
    def basic_validator_service(self, postData):
        errors = {}
        date = postData['service_date']
        time = postData['service_time']
        new_service_date = date + " " + time
        service_check = self.filter(service_date=new_service_date)
        if service_check:
            errors['service_date'] = 'Another service is already scheduled for this time. Please select a different day or time'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    phone = models.IntegerField()
    password = models.CharField(max_length=255)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Brand(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Car(models.Model):
    brand = models.ForeignKey(Brand, related_name="cars", on_delete = models.CASCADE)
    year = models.IntegerField()
    mileage = models.IntegerField()
    owner = models.ForeignKey(User, related_name="cars", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Service_Detail(models.Model):
    car = models.ForeignKey(Car, related_name="services", on_delete = models.CASCADE)
    service_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ServiceManager()