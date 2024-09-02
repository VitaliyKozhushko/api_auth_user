from django.contrib import admin
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

class MentorForm(forms.ModelForm):
  mentees = forms.ModelMultipleChoiceField(
    queryset=User.objects.filter(is_mentor=False, mentor__isnull=True,is_superuser=False),
    required=False,
    widget=admin.widgets.FilteredSelectMultiple('Mentees', is_stacked=False)
  )

  class Meta:
    model = User
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.instance.pk:
      self.was_mentor = self.instance.is_mentor
      self.fields['mentees'].initial = self.instance.mentees.all()

      mentees_queryset = User.objects.filter(is_mentor=False)
      mentees_queryset = mentees_queryset.filter(mentor=None) | mentees_queryset.filter(mentor=self.instance)
      self.fields['mentees'].queryset = mentees_queryset

  def save(self, commit=True):
    user = super().save(commit=False)
    user.save()

    if self.was_mentor and not user.is_mentor:
      mentees = User.objects.filter(mentor=user)

      for mentee in mentees:
        mentee.mentor = None
        mentee.save()
    else:
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