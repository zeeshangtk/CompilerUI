from django.conf.urls import url

from . import views

app_name = "compiler"

urlpatterns = [
    url(r'^$', views.run_program),
               ]