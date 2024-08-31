from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
  list_display = ('id', 'username', 'phone', 'email', 'is_mentor')
  search_fields = ('username', 'phone', 'email')
  list_filter = ('is_mentor',)

  fieldsets = BaseUserAdmin.fieldsets + (
    ('Mentor info', {'fields': ('is_mentor',)}),
  )

admin.site.register(User, UserAdmin)