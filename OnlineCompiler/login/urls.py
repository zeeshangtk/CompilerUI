from django.conf.urls import url

from . import views

app_name = "login"

user_controller = views.UserView()
urlpatterns = [
    url(r'^$', user_controller.login),
    url(r'^logout/$', user_controller.logout),
    url(r'^authenticate/$', user_controller.authenticate_user),
    url(r'^adduser/$', user_controller.add_user)
               ]