from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from accounts.utils import create_new_ref_number
from random import randint
from accounts import utils
from django.template.defaultfilters import slugify

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
               email=self.normalize_email(email),
               username=username,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
               email=self.normalize_email(email),
               username=username,
               password=password,
            )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User_Account(AbstractBaseUser):

    email               = models.EmailField(verbose_name="email", max_length=50, unique=True)
    username            = models.CharField(max_length=30, unique=True)
    date_joined         = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_activate         = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_student          = models.BooleanField(default=False)
    is_tutor            = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Tutor(User_Account):

    first_name          = models.CharField(max_length=50, blank=True)
    Last_name           = models.CharField(max_length=50, blank=True)
    GENDER_CHOICES      = (
                                ('M', 'Male'),
                                ('F', 'Female'),
                          )
    gender              = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Phone               = models.CharField(max_length = 10 , blank=True)
    profile_pic         = models.ImageField(upload_to='profile_image')
    About               = models.CharField(max_length = 200, blank=True)
    Country             = models.CharField(max_length = 10, blank=True)
    Experience          = models.CharField(max_length = 30, blank=True)
    Qualification       = models.CharField(max_length = 20, blank=True)
    slug                = models.SlugField(null=True, unique=True)

    class Meta:
        verbose_name = "Instructor"



    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('tutor_profile_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

class TutorialCategory(models.Model):

    tutorial_category = models.CharField(max_length=200)
    slug                = models.SlugField(blank=True,null=True, unique=True)

    class Meta:
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.tutorial_category

    def get_absolute_url(self):
        #return f"/accounts/Categories/{self.slug}"
        return reverse('Category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.tutorial_category)
        return super().save(*args, **kwargs)



class Series(models.Model):
    series_title = models.CharField(max_length=200)
    series_category = models.ForeignKey(TutorialCategory, verbose_name="Category", on_delete=models.CASCADE)
    series_instructor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    series_summary = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='Course_thumbnails',null=True)
    price = models.IntegerField(null=True)
    slug                = models.SlugField(null=True, unique=True,blank=True)

    class Meta:
        verbose_name = "Course"

    def __str__(self):
        return self.series_title



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.series_title + "-" + str(randint(0,100)))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        #return f"/accounts/series/{self.slug}/"
        return reverse('series_detail', kwargs={'slug': self.slug})


class Student(User_Account):
    first_name          = models.CharField(max_length=50, blank=True)
    Last_name           = models.CharField(max_length=50, blank=True)
    GENDER_CHOICES      = (
                                ('M', 'Male'),
                                ('F', 'Female'),
                          )
    gender              = models.CharField(max_length=1, choices=GENDER_CHOICES)
    Phone               = models.CharField(max_length = 10 , blank=True)
    profile_pic         = models.ImageField(upload_to='profile_image')
    Country             = models.CharField(max_length = 100, blank=True)
    slug                = models.SlugField(null=True, unique=True)
    course              = models.ManyToManyField(Series)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('student_profile_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)
"""
        @classmethod
        def add_course(cls, current_student, new_course):
            series, added = cls.objects.get_or_create(
            current_student = current_student
            )
            student.series.add(new_course)

        @classmethod
        def remove_course(cls, current_student, new_course):
            course, added = cls.objects.get_or_create(
            current_student = current_student
            )
            student.course.remove(new_course)

"""



class Video(models.Model):
    series = models.ForeignKey(Series,null=True, on_delete=models.CASCADE)
    video_title = models.CharField(max_length=100, verbose_name="Lesson Title")
    video_summary = models.CharField(max_length=500, verbose_name="Lesson Description")
    video_number = models.IntegerField(null=True, verbose_name="Lesson Number")
    videofile= models.FileField(upload_to='videos', null=True, verbose_name="Video")
    slug                = models.SlugField(null=True, unique=True,blank=True)

    class Meta:
        verbose_name = "Lesson"

    def __str__(self):
        return self.video_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.video_number) + "/" + self.video_title + "#" + str(randint(0,100)))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'slug': self.slug})
        #return f"/accounts/series/videos/{self.slug}"

class Question(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    video = models.ForeignKey(Video,null=True,on_delete=models.CASCADE)
    question_title = models.CharField(max_length=100)
    question_details = models.CharField(max_length=1000, verbose_name ="body")
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    slug                = models.SlugField(null=True,blank=True)


    def __str__(self):
        return self.question_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question_title + str(randint(0,100)))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'slug': self.slug})
        #return f"/accounts/Categories/series/video/question/{self.slug}"

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(User_Account,null=True,on_delete=models.CASCADE)
    ans = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    course = models.ForeignKey(Series,on_delete=models.CASCADE)
    student =  models.ForeignKey(Student,on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
            )
    rating = models.IntegerField(choices=CHOICES)
    review_date        = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.course.series_title + "-->" + self.student.username

class Transaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name = "student_pay")
    course = models.ForeignKey(Series, on_delete=models.CASCADE)
    Referrence_Number = models.CharField(max_length = 10,blank=True,editable=False,default=create_new_ref_number())
    amount = models.IntegerField(blank=True)
    payment_mode = models.CharField(max_length=20, default="Online")
    date = models.DateField(auto_now_add=True)
