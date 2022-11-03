from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    # to associate each customer with a user
    # if a user is deleted that customer also gets deleted
    user=models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name=models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=200, null=True)
    author=models.CharField(max_length=200, null=True)
    yearOfPublication=models.CharField(max_length=5, null=True)
    copies=models.IntegerField(null=True)
    
    description=models.CharField(max_length=10000, null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)

    # now a single book can have different tags and multiple tags can go to multiple books
    # so we need a many to many relationship
    tags=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


