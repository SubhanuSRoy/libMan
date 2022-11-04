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
        return self.title

class Issue(models.Model):
    
    # we want each issue to refer to customer so we need a foreign key
    # we want to make a 1 cust to many issues relation here
    # if in case a customer is deleted, then we just want to make this field as NULL
    customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)

    # we want each issue to refer to book so we need a foreign key
    # we want to make a 1 book to many issues relation here
    book = models.ForeignKey(Book,null=True,on_delete=models.SET_NULL)
    issue_date=models.DateTimeField(auto_now_add=True, null=True)
