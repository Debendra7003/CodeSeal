from django.contrib import admin
from django.urls import path,include
from .views import UserCreateView,login_view

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('singup/',UserCreateView.as_view(),name='singup'),
    path('login/',login_view,name='login'),

]