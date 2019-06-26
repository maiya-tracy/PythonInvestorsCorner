from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='landing'),
    url(r'^registration$', views.registration),
    url(r'^registration/processing$', views.registration_process),
    url(r'^login$', views.login, name='login'),
    url(r'^login/processing$', views.login_process),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^news$', views.news, name='news'),
    url(r'^investments$', views.investments),
    url(r'^investments/processing', views.investments_process),
    url(r'^chatroom/(?P<chatroomid>\d+)$', views.view_chatroom),
    url(r'^token', views.token, name='token'),
    url(r'^communities$', views.community),
    url(r'^logout$', views.logout, name='logout'),
    # url(r'^user/chatroom/add', views.add_chatroom),
    # url(r'^user/chatroom/add/processing$' views.add_chatroom_process),
]
