from django.urls import path
from . import views

app_name = "survey"

urlpatterns = [
    path("", views.survey_list, name="list"),
    path("<int:pk>/", views.survey_detail, name="detail"),
    path("<int:pk>/tesekkurler/", views.thank_you, name="thank_you"),
    path("kayit/", views.register, name="register"),
]
