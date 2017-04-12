from django.conf.urls import url
from django.contrib import admin
from .views import (
    match_detail_view,
    main_view,
    player_summary_view,
    search_view
    )

urlpatterns = [
    url(r'^$', main_view, name='home'),
    url(r'^matches/(?P<match_id>\d{10})', match_detail_view, name='match_detail'),
    url(r'^player/(?P<account_id>\d*)', player_summary_view, name='player_summary'),
    url(r'^search/(?P<search_id>\d*)', search_view, name='search_view'),



    
    
    

]
