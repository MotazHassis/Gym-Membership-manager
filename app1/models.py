from django.db import models
import bcrypt
import re
from datetime import date

class Cost(models.Model):
    monthly_fee=models.FloatField(default=0)
    daily_fee=models.FloatField(default=0)
    admin_code=models.CharField(max_length=64,default=567405021)
    user_code=models.CharField(max_length=64,default=1234)

class AdminManager(models.Manager):
    def basic_validator1(self, postData):
        errors={}
        if len(postData['fname']) < 2 :
            errors['fname']= 'First name should be more than 2 characters'
        if len(postData['lname']) < 2 :
            errors['lname']= 'last name should be more than 2 characters'
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']= 'Invalid Email Address'
        if len(postData['password']) < 8:
            errors['password']= 'Please Password must be at least 8 characters.'
        if postData['password'] != postData['confirm']:
            errors['confirm']= 'Password not match'
        return errors
    
class Admin(models.Model):
    lname=models.CharField(max_length=64)
    fname=models.CharField(max_length=64)
    email=models.CharField(max_length=255)
    password=models.TextField()
    type=models.CharField(max_length=64,default='user')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects= AdminManager()

class Member(models.Model):
    fname=models.CharField(max_length=64)
    lname=models.CharField(max_length=64)
    mobile=models.CharField(max_length=64)
    membership_type=models.CharField(max_length=64)
    start_membership_date=models.DateTimeField(blank=True, null=True)
    end_membership_date=models.DateTimeField(blank=True, null=True)
    avatar=models.ImageField(upload_to='image',default='image/default.jpg',blank=True)
    added_by=models.ForeignKey(Admin,related_name='members', on_delete=models.PROTECT)
    payed_amount=models.FloatField(default=0)
    status = models.BooleanField(default=True)
    address=models.CharField(max_length=64,default='j')
    membership_cost=models.FloatField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def is_expired(self):
        return date.today() > self.end_membership_date.date()
    def is_not_paid(self):
        return 130 > self.payed_amount
    def is_payed(self):
        cost1=Cost.objects.get(id=1)
        if self.membership_type=="شهري":
            return cost1.monthly_fee <= self.payed_amount
        else:
            return cost1.daily_fee <= self.payed_amount
    
class Item(models.Model):
    title=models.CharField(max_length=100)
    item_image=models.ImageField(upload_to='image',default='image/default.jpg',blank=True)
    total_quantity=models.IntegerField()
    available_quantity=models.IntegerField(default=0)
    sold_quantity=models.IntegerField(default=0)
    added_by=models.ForeignKey(Admin,related_name='items', on_delete=models.PROTECT)
    price = models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def is_empty(self):
        return self.available_quantity == 0