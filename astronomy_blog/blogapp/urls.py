from django.urls import path
from . import views
# from wagtail import urls as wagtail_urls

urlpatterns = [
    path('', views.home, name='home'),

    # path('', include(wagtail_urls)),
]