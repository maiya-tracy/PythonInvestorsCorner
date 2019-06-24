from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.home),
    url(r'^registration$', views.registration),
    url(r'^registration/processing$', views.registration_process),
    url(r'^login$', views.login),
    url(r'^login/processing$', views.login_process),
    url(r'^user/news$', views.news),
    # url(r'^user/news/')
    url(r'^user/investments$', views.investments),
    url(r'^user/investments/processing', views.investments_process)
    # url(r'^user/chatroom/add', views.add_chatroom),
    # url(r'^user/chatroom/add/processing$' views.add_chatroom_process),
]