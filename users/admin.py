from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import User, Instructor, Other

class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
@admin.register(User)
class UserAdmin(UserAdmin):
	form = UserChangeForm

	fieldsets = (
	        (None, {'fields': ('email', 'phone_number', 'password',)}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', )}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', )}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined', )}),
			
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide', ),
			'fields': ('email', 'phone_number', 'password1', 'password2', ),
		}),
	)
	list_display = ['email', 'first_name', 'last_name', 'is_staff', "phone_number", 'is_active']
	search_fields = ('email', 'first_name', 'last_name', )
	ordering = ('email', )
  
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
	model = Instructor
	list_display = ['username', 'first_name', 'last_name', 'email', 'campus']

@admin.register(Other)
class OtherAdmin(admin.ModelAdmin):
	model = Other
	list_display = ['username', 'first_name', 'last_name', 'campus']

	

