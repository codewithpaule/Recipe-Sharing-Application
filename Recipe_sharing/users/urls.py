# users/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('updateinfo/', update_personal_information, name='updateinfo'),
    path('changepass/', change_password, name='changepass'),
    path('logout/', logout_view, name='logout'),
]
