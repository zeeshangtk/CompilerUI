from django.apps import AppConfig


class CompilerConfig(AppConfig):
    name = 'compiler'
    base_url = "http://127.0.0.1:5000/"
    compiler_url = base_url+"compile"
