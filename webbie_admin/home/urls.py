from django.urls import path
from django.contrib.auth import views as auth_views
from . import user_permission
from . import module
from . import views
urlpatterns = [
    path('account/user-list/', user_permission.UserListView.as_view()),
    path('account/user-invite/', user_permission.UserCreateView.as_view(), name="user_invite"),
    path('account/user-update/<str:uid>/<str:token>', user_permission.UserUpdateView.as_view(), name='user_update'),
    path('account/user-permission/<int:id>', user_permission.UserPermissionView.as_view()),
    path('account/module-list/', module.ModuleListView.as_view(),name="module_list"),
    path('account/check-username/', user_permission.check_unique_user, name="check_username"),

    path('', views.index, name='index'),
   
    path('user_details/<int:id>', views.index, name='user_details'),

    path('billing/', views.billing, name='billing'),
    path('user_permission/', views.billing, name='user_permission'),
    path('user_staff/', views.billing, name='user_staff'),
    path('user_sale/', views.billing, name='user_sale'),
    path('user_subcription/', views.billing, name='user_subcription'),
    path('userdta/', views.billing, name='userdta'),



    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('subcription/', views.subcription, name='subcription'),
    path('subcription/add_subcription/', views.add_subcription, name='add_subcription'),

    path('profile/', views.display_data, name='profile'),


    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]

