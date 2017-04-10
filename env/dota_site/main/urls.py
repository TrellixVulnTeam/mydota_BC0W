from django.conf.urls import url
from django.contrib import admin
from .views import match_detail_view, main_view

urlpatterns = [
    url(r'^$', main_view, name='home'),
    url(r'^matches/(?P<match_id>\d{10})', match_detail_view, name='match_detail'),


    
    
    

]
