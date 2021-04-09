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
    path('', post_views.PostListView, name='post_list'),
    path('create/details/', post_views.PostCreateView.as_view(), name='post_create'),
    path('p/<int:pk>', post_views.SinglePostView, name='single_post_view'),
    path('comment/<int:pk>', post_views.CommentCreateView, name='post_comment_create'),
    path('reply/<int:pk>', post_views.ReplyCreateView, name='comment_reply_create'),
    path('search/', post_views.SearchView, name='search'),
    path('explore/', post_views.ExploreView.as_view(), name='explore'),
    path('admin/', admin.site.urls),

    path('like/<int:pk>/',post_views.LikeView.as_view(), name='post_like'),
    path('unlike/<int:pk>/',post_views.UnlikeView.as_view(), name='post_unlike'),
    path('share/search/',post_views.ShareProfileView, name='share_profile_search'),
    path('share/',post_views.ShareView.as_view(), name='post_share'),

    path('save/<int:pk>/',post_views.SaveView.as_view(), name='post_save'),
    path('unsave/<int:pk>/',post_views.UnsaveView.as_view(), name='post_unsave'),

    path('direct/inbox/', message_views.InboxListView, name='inbox_list'),
    path('direct/t/<int:pk>/', message_views.InboxDetailView, name='inbox_detail'),
    path('direct/profile/', message_views.InboxFindProfileView, name='inbox_find_profile'),
    path('direct/new/<int:pk>', message_views.InboxCreateView, name='inbox_create'),
    path('message/<int:pk>/', message_views.MessageCreateView, name='message_create'),
    path('direct/t/message/update/<int:pk>', message_views.MessageUpdateView, name='message_update'),


    path('notification/message/<int:pk>', notification_views.InboxNotificationView.as_view(), name='inbox_notification'),
    path('notification/<int:pk>', notification_views.NotificationView.as_view(), name='notification'),
    path('notification/display/<int:pk>', notification_views.NotificationDisplayView.as_view(), name='notification_display'),


    path('follow/', user_views.followView.as_view(), name='follow'),
    path('<str:username>/', user_views.profileView, name='profile'),
    path('<str:username>/saved/', user_views.savedDisplayView, name='saved'),
    path('accounts/emailsignup/', user_views.signupView, name='signup'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('accounts/edit/', user_views.editView, name='edit'),
    path('accounts/password/change', user_views.change_password, name='change_password'),
    path('accounts/login/', user_views.LoginView.as_view(template_name="user/login.html",authentication_form=LoginForm), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password/reset', auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"), name='password_reset'),
    path('accounts/password/reset/done', auth_views.PasswordResetDoneView.as_view(template_name="user/password_reset_done.html"), name='password_reset_done'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/password/reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
