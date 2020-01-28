from django.urls import path
from accounts import views
from django.contrib.auth.decorators import login_required
from .views import TutorProfileListView, TutorProfileDetailView, StudentProfileListView, StudentProfileDetailView, SearchResultsView, SeriesListView, SeriesDetailView,VideoDetailView, CategoryListView,CategoryDetailView,QuestionDetailView

urlpatterns = [
    path("register/",views.register,name="register"),
    path("registerstudent",views.registerstudent,name="registerstudent"),
    path("logout/",views.logout_view,name="logout"),
    path("login/",views.login_view,name="login"),
    path("usertype/",views.usertype,name="usertype"),
    path("studentprofile/",views.studentprofile,name="studentprofile"),
    path("edit-profile-tutor/",views.editprofile,name="editprofile"),
    path("edit-profile-student/<slug:slug>/",views.editprofilestudent,name="editprofilestudent"),
    path('tutor-profiles/<slug:slug>', TutorProfileDetailView.as_view(), name='tutor_profile_detail'),
    path('tutor-profiles/', TutorProfileListView.as_view(), name='tutor_profile_list'),
    path('student/profile/<slug:slug>', StudentProfileDetailView.as_view(), name='student_profile_detail'),
    path('student-profiles/', StudentProfileListView.as_view(), name='student_profile_list'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('series/',SeriesListView.as_view(),name="series_list"),
    path('series/<slug:slug>/', login_required(SeriesDetailView.as_view()), name='series_detail'),
    path('series/videos/<slug:slug>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('Categories/', CategoryListView.as_view(), name='Category_list'),
    path('Categories/<slug:slug>', views.CategoryDetailView.as_view(), name='Category_detail'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('series/review/<slug:slug>/',views.reviewform,name="reviewform"),
    path('course/payment-gate/?course=<slug:slug>?user=<str:username>/',views.payment,name="payment"),
    path('payment-success/<slug:slug>/<str:username>/',views.payment_success,name="payment_success"),
    path('mycourses/', views.mycourses, name="mycourses"),
    path('Categories/series/video/question/<slug:slug>', views.QuestionDetailView.as_view(), name='question_detail'),
    path('Categories/series/add/<slug:slug>/<str:username>/', views.addcourse, name='addcourse'),
    path('Categories/series/remove/<slug:slug>/<str:username>/', views.removecourse, name='removecourse'),


]
