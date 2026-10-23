from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path('signup', views.signup, name='signup'),
    path('signinstudent/', views.signinstudent, name='signinstudent'),
    path('signinmentor', views.signinmentor, name='signinmentor'),
    path('signupstudent', views.signupstudent, name='signupstudent'),
    path('signupmentor', views.signupmentor, name='signupmentor'),
    path('studenthomepage/<str:studentid>/', views.studenthomepage, name='studenthomepage'),
    path('searchtuition/', views.searchtuition, name = 'searchtuition'),
    path('mentorhomepage', views.mentorhomepage, name='mentorhomepage'),
    path('newtuition', views.newtuition, name='newtuition'),
    path('registertution', views.registertution, name='registertution'),
    path('updatestudentprofile/<str:studentid>/', views.updatestudentprofile, name='updatestudentprofile'),
    path('myeduclinic/updatestudentdata/<str:studentid>/', views.updatestudentdata, name='updatestudentdata'),
    path('updatetuition/<str:tuitioncode>/', views.updatetuition, name='updatetuition'),
    path('studenthomepage/<str:studentid>/updatetuition/<str:tuitioncode>/', views.updatetuition, name='updatetuition'),
    path('updatetuitiondata/<str:tuitioncode>/', views.updatetuitiondata, name='updatetuitiondata'),
    path('updatementor/<str:mentorid>/', views.updatementor, name='updatementor'),
    path('updatementordata/<str:mentorid>/', views.updatementordata, name='updatementordata'),
    path('deletetuition/<str:tuitioncode>/', views.deletetuition, name='deletetuition'),
    path('deletetuitiondata/<str:tuitioncode>/', views.deletetuitiondata, name='deletetuitiondata'),
    path('deletementor/<str:subjectcode>/', views.deletementor, name='deletementor'),
    path('deletementordata/<str:mentorid>/', views.deletementordata, name='deletementordata'),
]
