from django.urls import path
from apps.users.presentation.api.views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserMeView,
    CustomerProfileView,
    CookProfileView,
    UserAddressListCreateView,
)

urlpatterns = [
    path("register/",            UserRegisterView.as_view(),       name="user-register"),
    path("login/",               UserLoginView.as_view(),          name="user-login"),
    path("logout/",              UserLogoutView.as_view(),         name="user-logout"),
    path("me/",                  UserMeView.as_view(),              name="user-me"),
    path("me/customer-profile/", CustomerProfileView.as_view(),     name="user-customer-profile"),
    path("me/cook-profile/",     CookProfileView.as_view(),         name="user-cook-profile"),
    path("me/addresses/",        UserAddressListCreateView.as_view(), name="user-addresses"),
]
