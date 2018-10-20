from django.contrib import admin
from django.utils.functional import curry
# Register your models here.
from .models import Profile

class UserAdmin(admin.ModelAdmin):
    admin.site.register(Profile)
#def get_form(self, request, **kwargs):
#        form = super(UserAdmin, self).get_form(request, **kwargs)
#        return curry(form, current_user=request.user)'''
