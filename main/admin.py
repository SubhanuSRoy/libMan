from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(Issue)