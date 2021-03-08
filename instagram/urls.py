from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.forms import LoginForm
from django.contrib.auth import views as auth_views
from user import views as user_views
from post import views as post_views
from message import views as message_views
from notification import views as notification_views


urlpatterns = [
    path('', post_views.PostListView.as_view(), name='post_list'),
    path('p/<int:pk>', post_views.SinglePostView, name='single_post_view'),
    path('comment/<int:pk>', post_views.CommentCreateView, name='post_comment_create'),
    path('search/', post_views.SearchView, name='search'),
    path('admin/', admin.site.urls),
    
    path('like/<int:pk>/',post_views.LikeView.as_view(), name='post_like'),
    path('unlike/<int:pk>/',post_views.UnlikeView.as_view(), name='post_unlike'),
    
    path('save/<int:pk>/',post_views.SaveView.as_view(), name='post_save'),
    path('unsave/<int:pk>/',post_views.UnsaveView.as_view(), name='post_unsave'),

    path('direct/inbox/', message_views.InboxListView, name='inbox_list'),
    path('direct/t/<int:pk>/', message_views.InboxDetailView, name='inbox_detail'),
    ########################## path('direct/new/', message_views.InboxCreateView.as_view(), name='inbox_create'),
    path('message/<int:pk>/', message_views.MessageCreateView, name='message_create'),
    path('direct/t/message/update/<int:pk>', message_views.MessageUpdateView, name='message_update'),


    path('notification/message/<int:pk>', notification_views.InboxNotificationView.as_view(), name='inbox_notification'),
    path('notification/<int:pk>', notification_views.NotificationView.as_view(), name='notification'),
    path('notification/display/<int:pk>', notification_views.NotificationDisplayView.as_view(), name='notification_display'),


    path('<str:username>/', user_views.profileView, name='profile'),
    path('accounts/emailsignup/', user_views.signupView, name='signup'),
    path('accounts/edit/', user_views.editView, name='edit'),
    path('accounts/password/change', user_views.change_password, name='change_password'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="user/login.html"), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)