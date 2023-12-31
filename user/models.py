from django.db import models
from .constants import *
from django.contrib.auth.models import User
from book.models import *
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='info', on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2) 
    def __str__(self):
        return str(self.user.username)
    
class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length= 100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
    def __str__(self):
        return str(self.user.username)

class BorrowingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    borrowed_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    book_returned = models.BooleanField(default=False)