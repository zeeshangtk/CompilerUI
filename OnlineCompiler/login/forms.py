import logging

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.utils import InternalError
from django.forms.forms import Form

logger = logging.getLogger('django')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User

    username = forms.CharField(widget=forms.TextInput({ "placeholder": "Username" }))
    password = forms.CharField(widget=forms.PasswordInput({ "placeholder": "Password" }))
    first_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Name" }))
    email = forms.CharField(widget=forms.TextInput({ "placeholder": "Email-ID" }))


class UserForm(Form):

    class Meta:
        model = User

    username = forms.CharField(widget=forms.TextInput({ "placeholder": "Username" }))
    password = forms.CharField(widget=forms.PasswordInput({ "placeholder": "Password" }))
    first_name = forms.CharField(widget=forms.TextInput({ "placeholder": "Name" }))
    email = forms.CharField(widget=forms.TextInput({ "placeholder": "Email-ID" }))

    def create_user(self,request):
        form = UserForm(data=request.POST)
        logger.info("Adding user")

        self.__validate_form(form)
        try:
            user = self.__add_user_in_db(form)
            logger.info("The new user was saved successfully" + str(user))
            return "Added user successfully"
        except (IntegrityError,Exception) as e:
            logger.info("DB error while trying to add user" + str(e))
            raise InternalError("Error while adding user to "+str(e))

    def login_user(self, request):
        form = AuthenticationForm(data=request.POST)
        # Need to check this commented part
        # self.__validate_form(form)

        user = authenticate(username=form["username"].data,password=form["password"].data)
        if user is None:
            logger.info("Invalid user")
            return "Invalid username or password"
        login(request=request,user=user)
        logger.info("Found the user")

        return "User logged in sucessfully"

    def __validate_form(self, form):
        logger.info("The binding of the form is "+str(form.is_bound))
        logger.info("The validation of the form is "+str(form.is_valid()))
        logger.info("The errors of the form is "+str(form.errors))

        if not form.is_valid():
            raise ValidationError("The form was invalid ")


    def __add_user_in_db(self, form):
        username = form["username"].data
        password = form["password"].data
        first_name = form["first_name"].data
        email = form["email"].data

        user = User.objects.create_user(username=username, first_name=first_name, email=email, password=password)
        return user
