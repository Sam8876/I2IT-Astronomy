from django.urls import path
from . import views
# from wagtail import urls as wagtail_urls

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    # path('', include(wagtail_urls)),
]