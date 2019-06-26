from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^registration$', views.registration),
    url(r'^registration/processing$', views.registration_process),
    url(r'^login$', views.login),
    url(r'^login/processing$', views.login_process),
    url(r'^news$', views.news),
    url(r'^investments$', views.investments),
    url(r'^investments/processing', views.investments_process),
    url(r'^chatroom/(?P<chatroomid>\d+)$', views.view_chatroom),
    url(r'^token', views.token, name='token'),
    url(r'^community$', views.community),
    url(r'^logout$', views.logout),
    # url(r'^user/chatroom/add', views.add_chatroom),
    # url(r'^user/chatroom/add/processing$' views.add_chatroom_process),
]
