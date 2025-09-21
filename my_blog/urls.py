from django.urls import path
from . import views
urlpatterns = [
    path('',views.PostListView,name='post_list'),
    path('post/<int:pk>/',views.PostDetailView,name='post_detail'),
    path('like/<int:id>/',views.LikePost,name='like_post'),
    path('register/',views.register_view,name='register'),   
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('create/',views.create_post,name='create_post'),
    path('edit/<int:pk>/',views.edit_post,name='edit_post'),
    path('delete/<int:pk>/',views.delete_post,name='delete_post')
         
]