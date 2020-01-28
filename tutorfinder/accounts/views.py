from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from accounts.forms import RegistrationForm, AuthenticationForm, RegistrationFormStudent,QuestionForm, ProfileEditForm,SeriesForm,AnswerForm, StudentProfileEditForm, UploadVideoForm, ReviewForm
from accounts.models import Tutor, Student, Series, Video, TutorialCategory, Question, Answer, Review, Transaction
from django.views.generic import ListView, DetailView, FormView, CreateView, View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg


def register(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'register.html', context)

def registerstudent(request):
    context = {}
    if request.POST:
        form = RegistrationFormStudent(request.POST, request.FILES)
        if form.is_valid():
            regs = form.save(commit=False)
            regs.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form_student'] = form
    else:
        form = RegistrationFormStudent()
        context['registration_form_student'] = form

    return render(request, 'student_registration.html', context)

def usertype(request):
    return render(request, 'usertype.html')

def tutorprofile(request):
    return render(request, 'tutorprofile.html')

def studentprofile(request):
    return render(request, 'studentprofile.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):

    context = {}
    cat = TutorialCategory.objects.all()
    context['cat'] = cat

    user = request.user
    if user.is_authenticated:
       return redirect("home")

    if request.POST:
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if user.is_student == True:
                    return redirect("home")
                else:
                    return redirect("myprofile")

    else:
        form = AuthenticationForm()

    context['login_form'] = form
    return render(request, 'login.html', context)

def editprofile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.tutor)
        if form.is_valid():
            form.initial = {
                "first_name": request.POST['first_name'],
                "Last_name": request.POST['Last_name'],
                "Phone": request.POST['Phone'],
                "Qualification": request.POST['Qualification'],
                "Country": request.POST['Country'],
                "About": request.POST['About'],
                "profile_pic": request.POST['profile_pic'],
                            }

            form.save()
            context['success_message'] = "Updated"
    else:
        form = ProfileEditForm(
                initial = {
                "first_name": request.user.tutor.first_name,
                "Last_name": request.user.tutor.Last_name,
                "Phone": request.user.tutor.Phone,
                "Qualification": request.user.tutor.Qualification,
                "Experience": request.user.tutor.Experience,
                "Country": request.user.tutor.Country,
                "About": request.user.tutor.About,
                "profile_pic": request.user.tutor.profile_pic,
                }
            )
    context['edit_form'] = form
    return render(request, 'editprofile.html', context)

def editprofilestudent(request,slug):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    stu = get_object_or_404(Student, slug=slug)
    if request.POST:
        form = StudentProfileEditForm(request.POST, request.FILES, instance=request.user.student)
        if form.is_valid():
            form.save()
    else:
        form = StudentProfileEditForm(
                initial = {
                "first_name": request.user.student.first_name,
                "Last_name": request.user.student.Last_name,
                "Phone": request.user.student.Phone,
                "Country": request.user.student.Country,
                "profile_pic": request.user.student.profile_pic,
                }
            )
    context['edit_form'] = form
    context['stu'] = stu
    return render(request, 'editprofilestudent.html', context)



class TutorProfileListView(ListView):
    model = Tutor
    template_name = 'tutor_profile_list.html'



class TutorProfileDetailView(DetailView):
    model = Tutor
    template_name = 'tutor_profile_detail.html'


class StudentProfileListView(ListView):
    model = Student
    template_name = 'student_profile_list.html'



class StudentProfileDetailView(DetailView):
    model = Student
    template_name = 'student_profile_detail.html'

    def get_context_data(self,**kwargs):
        context = super(StudentProfileDetailView, self).get_context_data(**kwargs)
        cat = TutorialCategory.objects.all()
        context['cat'] = cat
        context['student'] = Student.objects.filter(id=self.request.user.id)
        context['tra'] = Transaction.objects.filter(student=self.request.user)
        return context





class SearchResultsView(ListView):
    model = Series
    template_name = 'search_results.html'

    def get_queryset(self):
        context = {}
        query = self.request.GET.get('q')
        object_list = Series.objects.filter(
        Q(series_title__icontains=query)
        )

        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['temp'] = self.request.GET.get('q')
        return context


class SeriesListView(ListView):
    model = Series
    queryset = Series.objects.all()
    template_name = 'series_list.html'


    def get_context_data(self,**kwargs):
        context = super(SeriesListView,self).get_context_data(**kwargs)
        context['cat'] = TutorialCategory.objects.all()
        return context




class SeriesDetailView(View):
    #login_url = 'accounts/login/'
    def get(self, request, *args, **kwargs):
        form = UploadVideoForm()
        review_form = ReviewForm()
        cat = TutorialCategory.objects.all()

        series = get_object_or_404(Series, slug=kwargs['slug'])
        avg = Review.objects.filter(course=series).aggregate(Avg('rating'))
        if Review.objects.filter(course=series).exists():
            rev = True
        else:
            rev = False

        if Video.objects.filter(series=series).exists():
            novid = False
        else:
            novid = True

        if request.user.is_student == True:
            if series.student_set.filter(username=request.user.student.username).exists():
                ob = True
            else:
                ob = False
            context = {'series': series, 'form':form, 'ob':ob, 'novid':novid ,'review_form':review_form,'rev':rev, 'avg':avg, 'cat':cat }

            if Review.objects.filter(student=request.user.student,course=series).exists():
                student_review = True
            else:
                student_review = False
            context = {'series': series, 'form':form, 'ob':ob, 'review_form':review_form,'novid':novid, 'rev':rev, 'avg':avg, 'student_review':student_review ,'cat':cat}


        elif series.series_instructor == request.user.tutor:
            is_instructor = True

            context = {'series': series, 'form':form, 'review_form': review_form,'novid':novid, 'rev':rev, 'avg':avg,'is_instructor': is_instructor , 'cat':cat}

        else:
            context = {'series': series, 'form':form, 'review_form': review_form,'novid':novid, 'rev':rev, 'avg':avg , 'cat':cat}

        return render(request,'series_detail.html',context)

    def post(self, request, *args, **kwargs):

        form = UploadVideoForm(request.POST or None, request.FILES or None)


        if form.is_valid():
            ser = get_object_or_404(Series, slug=kwargs['slug'])
            ob = form.save(commit=False)
            ob.series = ser
            ob.save()
        else:
            form = UploadVideoForm()
            return HttpResponseRedirect(self.request.path_info)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        #return render(request,'series_detail.html', {'form': form})




def reviewform(request,slug):
    review_form = ReviewForm(request.POST or None)
    if review_form.is_valid():
        cou = get_object_or_404(Series, slug=slug)
        rev =  review_form.save(commit=False)
        rev.student = request.user.student
        rev.course = cou
        rev.save()
    else:
        review_form = ReviewForm()

    #return render(request, 'series_detail.html', {'review_form': review_form})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return SeriesDetailView.as_view(request)


"""
class VideoDetailView(DetailView):
    model = Video
    template_name = 'video.html'

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        context['question'] = Question.objects.all()
        return context
"""

class VideoDetailView(View):


    def get(self, request, *args, **kwargs):
        form = QuestionForm()
        video = get_object_or_404(Video, slug=kwargs['slug'])
        series = get_object_or_404(Series, id=video.series.id)
        cat = TutorialCategory.objects.all()
        question = Question.objects.filter(video__pk=video.id)
        context = {'video': video, 'form':form, 'question':question, 'series':series, 'cat':cat}
        return render(request,'video.html',context)

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form     = QuestionForm(request.POST or None)
            if form.is_valid():
                video = get_object_or_404(Video, slug=kwargs['slug'])
                instance =  form.save(commit=False)
                instance.student = request.user.student
                instance.video = video
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)
                #return HttpResponseRedirect(self.request.path_info)
        #return render(request,'video.html', { 'form': form  })




class CategoryListView(ListView):
    model = TutorialCategory
    template_name = 'Category_list.html'

class CategoryDetailView(DetailView):
    model = TutorialCategory
    template_name = 'Category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['cat'] = TutorialCategory.objects.all()
        context['series'] = Series.objects.all()
        return context



def myprofile(request):
    context = {}
    cat = TutorialCategory.objects.all()
    form = SeriesForm(request.POST, request.FILES)
    if request.POST:
        if form.is_valid():
                ser =  form.save(commit=False)
                ser.series_instructor = request.user.tutor
                ser.save()



        else:
                form = SeriesForm()

    #context['tutor'] = Tutor.objects.all()
    context['cat'] = cat
    context['form'] = form
    context['series'] = Series.objects.filter(series_instructor__pk=request.user.id)
    return render(request, 'myprofile.html', context)



#class QuestionDetailView(DetailView):
    #model = Question
    #template_name = 'question.html'

    #def get_context_data(self, **kwargs):
        #context = super(QuestionDetailView, self).get_context_data(**kwargs)
        #context['answer'] = Answer.objects.all()
        #return context

class QuestionDetailView(View):

    def get(self, request, *args, **kwargs):
        form = AnswerForm()
        question = get_object_or_404(Question, slug=kwargs['slug'])
        answer_count = Answer.objects.filter(question=question).count()
        context = {'question': question, 'form':form, 'answer_count':answer_count}
        return render(request,'question.html',context)


    def post(self, request, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form     = AnswerForm(request.POST or None)
            if form.is_valid():
                quest = get_object_or_404(Question, slug=kwargs['slug'])
                instance =  form.save(commit=False)
                instance.user = request.user
                instance.question = quest
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)





            #return HttpResponseRedirect(self.request.path_info)
        #return render(request,'question.html', { 'form': form  })
"""
def add_cou(request,pk):
    new_course = Series.objects.get(slug=slug)
    Student.add_course(request.user.student, new_course)
    return Redirect('series_details')

def remove_cou(request,pk):
    new_course = Series.objects.get(pk=pk)
    Student.remove_course(request.user, new_course)
    return HttpResponseRedirect(self.request.path_info)
"""
def addcourse(request,slug,username):

    stu = get_object_or_404(Student, username=request.user.student)
    cou = get_object_or_404(Series, slug=slug)
    #cou, status = Series.objects.get_or_create(pk=pk)
    #student, status = Student.objects.get_or_create(request.user.student)

    transaction = Transaction.objects.create(student=stu, course=cou, amount=cou.price)
    transaction.save()

    stu.course.add(cou)
    stu.save()



    #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return HttpResponseRedirect(request.path_info)
    return render(request, 'payment_success.html', {'stu':stu, 'cou':cou })

def removecourse(request,slug,username):

    stu = get_object_or_404(Student, username=request.user.student)
    cou = get_object_or_404(Series, slug=slug)
    #stu = Student.objects.get(user=request.user)
    #cou, status = Series.objects.get_or_create(pk=pk)
    #student, status = Student.objects.get_or_create(request.user.student)


    stu.course.remove(cou)
    stu.save()

    #return render(request, 'removecourse.html')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return render(request, 'payment_success.html', {'stu':stu, 'cou':cou })

def payment(request,slug,username):

    stu = get_object_or_404(Student, username=request.user.student)
    cou = get_object_or_404(Series, slug=slug)


    return render(request, 'payment.html', {'stu':stu, 'cou':cou})

def payment_success(request):
    return render(request, 'payment_success.html')

def mycourses(request):
    cat = TutorialCategory.objects.all()
    t = Transaction.objects.filter(student=request.user.student)
    return render (request, 'mycourses.html', {'t':t, 'cat':cat})
