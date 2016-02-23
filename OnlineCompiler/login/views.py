import logging

from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from .forms import LoginForm,UserForm


logger = logging.getLogger('django')

class UserView():

    def logout(self,request):
        user_name = request.user
        logger.info("Logging out the user" + str(user_name))
        logout(request)
        return HttpResponse("The user " + str(user_name) + " has been logged out")

    def login(self,request):
        context = {"form":LoginForm()}
        logger.info("Got the logni page")

        return render(request, 'login.html', context)

    def authenticate_user(self,request):
        # TODO make UserForm a member variable
        # TODO authentiate_user should return true or false
        logger.info("Now authenticating the user")
        if "sucessfully" in  UserForm().login_user(request):
           return redirect("/compile/")
        return HttpResponse(UserForm().login_user(request))

    def add_user(self,request):
        if request.method == 'POST':
            # TODO make UserForm a member variable
            response_string = UserForm().create_user(request)
            return HttpResponse(response_string)
        else:
            context = {"form":UserForm()}
            return render(request,'adduser.html',context)

