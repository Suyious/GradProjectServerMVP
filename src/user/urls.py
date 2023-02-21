from django.urls import path
from .views import SignUp, LogIn, GetUser

urlpatterns = [
    path('login/', LogIn.as_view(), name="login"),
    path('signup/', SignUp.as_view(), name="signup"),
    path('me/', GetUser.as_view(), name="me"),
]
