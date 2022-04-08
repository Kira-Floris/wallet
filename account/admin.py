from django.contrib import admin
from .models import *

# Register your models here.

obj = [User]

for o in obj:
	admin.site.register(o)