from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>', views.UserProfileView.as_view(), name ='profile'),
    path('follow/<int:user_id>', views.FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>', views.UnfollowUserView.as_view(), name='unfollow'),
    path('followers/<int:user_id>', views.UserGetFollowersView.as_view(), name='get_followers'),
    path('followings/<int:user_id>', views.UserGetFollowingsView.as_view(), name='get_followings'),
    path('edit_user', views.EditProfileView.as_view(), name='edit_user')
]