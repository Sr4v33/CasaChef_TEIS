from django.urls import path
from apps.users.presentation.api.views import (
    UserRegisterView,
    UserMeView,
    CustomerProfileView,
    CookProfileView,
)

urlpatterns = [
    path("register/",               UserRegisterView.as_view(),   name="user-register"),
    path("me/",                     UserMeView.as_view(),          name="user-me"),
    path("me/customer-profile/",    CustomerProfileView.as_view(), name="user-customer-profile"),
    path("me/cook-profile/",        CookProfileView.as_view(),     name="user-cook-profile"),
]