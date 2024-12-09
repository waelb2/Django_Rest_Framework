from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.product_view),
    path("", views.product_view),
]
