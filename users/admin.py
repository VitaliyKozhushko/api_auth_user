from django.contrib import admin
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

class MentorForm(forms.ModelForm):
  mentees = forms.ModelMultipleChoiceField(
    queryset=User.objects.filter(is_mentor=False, mentor__isnull=True),
    required=False,
    widget=admin.widgets.FilteredSelectMultiple('Mentees', is_stacked=False)
  )

  class Meta:
    model = User
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.instance.pk:
        self.fields['mentees'].initial = self.instance.mentees.all()
        print(self.instance.mentees.all())

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if email:
      if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
        raise ValidationError('Пользователь с таким email уже существует.')
    return email

  def save(self, commit=True):
    user = super().save(commit=False)
    user.save()

    User.objects.filter(mentor=self.instance).update(mentor=None)

    for mentee in self.cleaned_data.get('mentees', []):
      mentee.mentor = self.instance
      mentee.save()

    return user

class UserAdmin(BaseUserAdmin):
  form = MentorForm
  list_display = ('id', 'username', 'phone', 'email', 'is_mentor')
  search_fields = ('username', 'phone', 'email')
  list_filter = ('is_mentor',)

  fieldsets = BaseUserAdmin.fieldsets + (
    ('Mentor info', {'fields': ('is_mentor',)}),
  )

  def get_fieldsets(self, request, obj=None):
    fieldsets = super().get_fieldsets(request, obj)
    if obj and obj.is_mentor:
      return fieldsets + (
        ('Mentees', {'fields': ('mentees',)}),
      )
    return fieldsets

  def get_queryset(self, request):
    return super().get_queryset(request).prefetch_related('mentees')

admin.site.register(User, UserAdmin)