from django.urls import path
from . import views


urlpatterns = [
    path('', views.new, name='new'),
    path('<slug:category_slug>/', views.new, name='articles_by_category'),
    path('<slug:category_slug>/<slug:article_slug>/', views.article_detail, name='article_detail')
]
