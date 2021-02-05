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
from django.urls import path, include

from apps.user_graph import views

urlpatterns = [
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/signup/", views.signup, name="signup"),
    path("ugraph", views.show_user_graph, name="show_user_graph"),
    path("ugraph/add", views.add_link, name="add_link"),
    path("ugraph/del/<int:link_id>", views.remove_link, name="remove_link"),
]
