from django                     import forms
from django.contrib             import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin  import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms  import ReadOnlyPasswordHashField

from .models import Item
from .models import Concept
from .models import Bloom
from .models import Level
from .models import ItemDep
from .models import Code
from .models import ItemSet
from .models import CourseItemSet
from .models import MyUser
from .models import Response
from .models import Course
from .models import CourseUser

admin.site.register(Code)
admin.site.register(Level)
admin.site.register(Concept)
admin.site.register(Bloom)
admin.site.register(Item)
admin.site.register(ItemSet)
admin.site.register(ItemDep)
admin.site.register(Course)
admin.site.register(CourseUser)
admin.site.register(CourseItemSet)
admin.site.register(Response)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
    #   ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions',   {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering      = ('email',)
    filter_horizontal = ()

admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)

#ModelAdmin.save_as=True
