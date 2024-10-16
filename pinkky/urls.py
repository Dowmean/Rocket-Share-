from django.urls import path
from pinkky.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', post_create, name='post'),
    path('', post_list, name='post_list'),
    path('list/user', post_list_user, name='post_list_user'),
    path('edit/<int:post_id>/', post_edit, name='post_edit'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('delete/<int:post_id>/', post_delete, name='post_delete'),
    path('save-location/', save_location, name='save-location'),
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)