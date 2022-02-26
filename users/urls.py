from django.urls import path, re_path
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetView
from allauth.account.views import ConfirmEmailView
from .views import (
    InstructorRegistrationView, 
    InstructorAccountView,
    InstructorAccountDeleteView,
    OtherRegistrationView, 
    OtherAccountDeleteView,
    OtherAccountView,

    )


urlpatterns = [
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    # path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),


    path('verify-email/',VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(), name='account_confirm_email'),

    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('registration/instructor/', InstructorRegistrationView.as_view(), name='register-instructor'),
    path('registration/other/', OtherRegistrationView.as_view(), name='register-other'),


    path('user/profile/<int:pk>', InstructorAccountView.as_view(), name = 'instructor_profile'),
    path('user/profile/<int:pk>/delete', InstructorAccountDeleteView.as_view(), name = 'instructor_profile_delete'),
    path('other/profile/<int:pk>', OtherAccountView.as_view(), name = 'other_profile'),
    path('other/profile/<int:pk>/delete', OtherAccountDeleteView.as_view(), name = 'other_profile_delete'),


    ]