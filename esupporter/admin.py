from django.contrib import admin

# Register your models here.
from .models import User, Question, Company, ES

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Company)
admin.site.register(ES)


