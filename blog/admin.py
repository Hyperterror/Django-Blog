from django.contrib import admin
from .models import Post, User, Category, Tag
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
  model=User
  list_display=["email","first_name","last_name","is_staff"]
  search_fields=['email']
admin.site.register(User,CustomUserAdmin)
admin.site.register(Post)

admin.site.register(Category)
admin.site.register(Tag)
