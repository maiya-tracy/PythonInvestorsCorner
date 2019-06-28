from django.conf.urls import url, include
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.home, name='landing'),
    url(r'^registration$', views.registration),
    url(r'^registration/processing$', views.registration_process),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/processing$', views.login_process),
    url(r'^settings/$', views.settings_page, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^news$', views.news, name='news'),
    url(r'^investments$', views.investments),
    url(r'^investments/update_price$', views.update_price),  #update watched stocks
    url(r'^investments/processing', views.investments_process),   #<--- DO WE EVER USE THIS?
    url(r'^add_stock$', views.add_stock, name='add_stock'),  #Jack - add stock route
    url(r'^paperstocks$', views.paper_stocks),
    url(r'^chatroom/(?P<chatroomid>\d+)$', views.view_chatroom),
    url(r'^token', views.token, name='token'),
    url(r'^communities$', views.community),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^fb_session$', views.fb_log, name='fb_session'),
    # url(r'^user/chatroom/add', views.add_chatroom),
    # url(r'^user/chatroom/add/processing$' views.add_chatroom_process),
]
