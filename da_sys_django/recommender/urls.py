from django.urls import path
from recommender import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('setup', views.Setup.as_view()),
    path('record', views.Record.as_view(), name='record'),
    path('get/records', views.GetRecord.as_view()),
]
