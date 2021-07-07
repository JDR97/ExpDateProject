from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', views.adminview, name='adminview'),
    path('adminauth/', views.authenticateadmin, name='adminauth'),
    path('adminhome/', views.adminhome, name='adminhome'),
    path('adminlogout/', views.logoutadmin, name='adminlogout'),
    path('addingcustomers/', views.addcustomer, name='addingcustomers'),
    path('deletecustomer/<int:customerpk>/', views.deletecustomer, name='deletecustomer'),
    path('', views.index, name='index'),
    path('signings/', views.signings, name='signings'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('userlogin/', views.usersignin, name='userlogin'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('userhome/', views.userhome, name='userhome'),
    path('userauth', views.authenticateuser, name='userauth'),
    path('userlogout', views.userlogout, name='userlogout'),
    path('deleteuser/<int:useridpk>/', views.deleteuser, name='deleteuser'),
    path('edituser/<int:customerpk>/', views.edituser, name='edituser'),
    path('editting/<int:customerpk>/', views.editting, name='editting'),
    path('newentry/', views.takingphoto, name='newentry'),
    path('productentry/', views.productentry, name='productentry'),
    path('deleteproduct/<int:productidpk>/', views.deleteproduct, name='deleteproduct'),
    path('shareproduct/<int:productidpk>/', views.shareproduct, name='shareproduct'),
    path('notification/', views.notification, name='notification'),
    path('feed/', views.feed, name='feed'),
    path('contact/<str:contactto>/', views.contact, name='contact'),
    path('storemsg/<str:contactto>/', views.storemsg, name='storemsg'),
    path('notifytext/', views.notifytext, name='notifytext'),

]

#urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)