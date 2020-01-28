from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User_Account, Tutor, Student, Video, TutorialCategory, Series, Question, Answer, Review, Transaction

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username','date_joined', 'last_login','is_admin', 'is_tutor', 'is_student')
    search_fields = ('email','username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class TutorAdmin(UserAdmin):
    list_display = ('first_name', 'Last_name','email', 'username', 'date_joined')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class StudentAdmin(UserAdmin):
    list_display = ('first_name', 'Last_name','email', 'username', 'date_joined')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Tutor, TutorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Video)
admin.site.register(Series)
admin.site.register(TutorialCategory)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Review)
admin.site.register(Transaction)
