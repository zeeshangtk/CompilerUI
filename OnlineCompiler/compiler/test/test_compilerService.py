from unittest import TestCase

from django.http.response import HttpResponse
from mock.mock import MagicMock

from ..service import CompilerService,RestClient


class TestCompilerService(TestCase):

    def test_should_print_a_simple_hi(self):
        rest_client = RestClient()
        rest_client.post_data = MagicMock()
        output_content = b"hi"
        expeted_response  = HttpResponse(content=output_content)
        expeted_response.status_code = 200
        rest_client.post_data.return_value = expeted_response

        service = CompilerService(rest_client)
        actual_output =  service.run_code("print('hi')", "python3")
        self.assertEqual(output_content, actual_output)

    def test_should_throw_a_runtime_exception_when_status_code_is_not_200(self):
        rest_client = RestClient()
        rest_client.post_data = MagicMock()
        output_content = b""
        expeted_response  = HttpResponse(content=output_content)
        expeted_response.status_code = 500
        rest_client.post_data.return_value = expeted_response
        service = CompilerService(rest_client)
        self.assertRaises(RuntimeError,service.run_code,"print('hi')", "python3")

