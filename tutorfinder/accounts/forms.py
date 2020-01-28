from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.forms import ModelChoiceField

from accounts.models import User_Account, Tutor, Student,Series,Video,Answer,Question, Review

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a vaild email address')
    is_tutor = forms.BooleanField(required=True, initial=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True)
    class Meta:
        model = Tutor
        fields = ("email", "username", "password1", "password2","first_name","Last_name","gender","Phone","profile_pic","Experience","Qualification","Country","About","is_tutor")

class RegistrationFormStudent(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a vaild email address')
    is_student = forms.BooleanField(required=True, initial=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True)
    class Meta:
        model = Student
        fields = ("email", "username", "password1", "password2","first_name","Last_name","gender","Phone","profile_pic","Country","is_student")


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget = forms.PasswordInput)

    class Meta:
        model = User_Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ('first_name', 'Last_name', 'Phone', "profile_pic","Qualification","Experience", "Country","About")

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Tutor.objects.exclude(pk=self.instance.pk).get(email=email)
            except Tutor.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Tutor.objects.exclude(pk=self.instance.pk).get(username=username)
            except Tutor.DoesNotExist:
                return username
            raise forms.ValidationError('username "%s" is already in use.' % email)

class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'Last_name', 'Phone', "profile_pic", "Country")

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Student.objects.exclude(pk=self.instance.pk).get(email=email)
            except Student.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Student.objects.exclude(pk=self.instance.pk).get(username=username)
            except Student.DoesNotExist:
                return username
            raise forms.ValidationError('username "%s" is already in use.' % email)

class SeriesForm(ModelForm):
    class Meta:
        model = Series
        exclude = ["slug","series_instructor"]

    def createseries(request):
        form = SeriesForm(request.POST)
        if request.method == 'POST':
            if form.is_valid:
                ser =  form.save(commit=False)
                ser.series_instructor = request.user.tutor
                ser.save()


class UploadVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ["video_title", "video_summary","videofile","video_number"]


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ["ans"]

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_title","question_details"]

class ReviewForm(ModelForm):
    CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
            )
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=True)
    class Meta:
        model = Review
        fields = ["review", "rating"]
