from django.urls import path
from . import views

urlpatterns = [
    path('contatti', views.newContact, name='newContact'),
    #path('showDigest/<int:pk>', views.showDigest, name='showDigest')

]
