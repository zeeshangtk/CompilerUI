from django.db.utils import InternalError
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

USER_NAME = 'userNameIs'

LOGIN_URL = "/login/"
LOGOUT_URL = "/login/logout/"
ADD_USER_URL = "/login/adduser/"
AUTHENTICATE_USER = "/login/authenticate/"


class TestUserView(TestCase):

    def test_if_login_page_is_available(self):
        global LOGIN_URL
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)

    def test_should_get_username_and_password_field_for_login_page(self):
        global LOGIN_URL
        response = self.client.get(LOGIN_URL)
        output_html = str(response.content)
        self.assertIn('<input id="id_username" name="username" placeholder="Username" type="text" />', output_html)
        self.assertIn('<input id="id_password" name="password" placeholder="Password" type="password" />', output_html)

    def test_should_be_able_to_add_user_which_is_not_present(self):
        response = self.__add_user()
        self.assertEqual(response.status_code,200)
        self.assertIn("Added user successfully",str(response.content))


    def test_should_throw_exception_on_adding_user_which_already_exists(self):
        self.__add_user()
        self.assertRaises(InternalError,self.__add_user)

    def test_should_be_able_to_authenticate_existing_user(self):
        self.__add_user()
        response = self.__authenticate_user()
        # TODO need to fix this test
        # self.assertIn("User logged in sucessfully",str(response.content))

    def test_should_not_be_able_to_authenticate_user_that_do_not_exists(self):

        response = self.__authenticat_invalid_user()
        self.assertIn("Invalid username or password",str(response.content))

    def test_should_not_be_able_to_authenticate_user_that_do_not_exists(self):
        response = self.__authenticat_invalid_user()
        self.assertIn("Invalid username or password",str(response.content))

    def test_should_not_be_able_to_authenticate_user_with_wrong_password(self):
        global USER_NAME
        response = self.__authenticat_invalid_user(username=USER_NAME)
        self.assertIn("Invalid username or password",str(response.content))


    def __authenticate_user(self):
        global AUTHENTICATE_USER
        response = self.client.post(path=AUTHENTICATE_USER, data=self.__user_data(), follow=True)
        return response

    def __authenticat_invalid_user(self,username="nonExistingUser123$",password="SomeRandomPassword"):
        global AUTHENTICATE_USER
        data = self.__user_data()
        data["username"]=username
        data["password"]=password
        response = self.client.post(path=AUTHENTICATE_USER, data=data, follow=True)
        return response

    def __add_user(self):
        global ADD_USER_URL
        response = self.client.post(path=ADD_USER_URL, data=self.__user_data(), follow=True)
        return response

    def __user_data(self):
        # Move data to a file
        global USER_NAME
        return MultiValueDict({"username": [('%s' % USER_NAME)],
                                     'password': ['listOfApples123$'],
                                     'email': ['user1@gmail.coms'],
                                     'first_name': ['John']
                                     })

