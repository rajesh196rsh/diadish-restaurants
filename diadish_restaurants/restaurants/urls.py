from django.urls import path
from .views import home_page


urlpatterns = [
    path('', home_page),
    path('<str:latitude>/<str:longitude>/<str:param>', home_page),
]