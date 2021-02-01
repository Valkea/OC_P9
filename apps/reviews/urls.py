"""litereview/flux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from apps.reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.main_reviews, name="main_reviews"),
    path("ticket/", views.add_ticket, name="add_ticket"),
    path("ticket/<int:ticket_id>", views.add_ticket, name="edit_ticket"),
    path("review/", views.new_review, name="new_review"),
    path("review/<int:review_id>", views.add_review, name="edit_review"),
    path("review/ticket/<int:ticket_id>", views.add_review, name="add_review"),
]
