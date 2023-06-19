from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('detail/<int:post_id>', views.PostDetailView.as_view(), name='detail'),
    path('edit/<int:post_id>', views.PostEditView.as_view(), name='edit'),
    path('create/', views.CreatePostView.as_view(), name='create'),
    path('bid/<int:post_id>', views.TakeBidView.as_view(), name='bid'),
    path('like/<int:post_id>', views.PostLikeView.as_view(), name='like'),
    path('delete/<int:post_id>', views.PostDeleteView.as_view(), name='delete'),
    path('reply/<int:post_id>/<int:comment_id>', views.AddReplyCommentView.as_view(), name='reply'),
]