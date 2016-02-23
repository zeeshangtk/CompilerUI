from django.core.exceptions import ValidationError
from django.forms.forms import Form
from django import forms
import requests as rest_client

from .service import CompilerService,RestClient


class ProgramInputForm(Form):
    class Meta:
        fields=("program")

    program = forms.CharField(widget=forms.Textarea({ "placeholder": "Code", }))

    def run_program(self,request):
        form = ProgramInputForm(data=request.POST)

        if not form.is_valid():
            raise ValidationError("The form was invalid ")

        program_code = form["program"].data
        # TODO remove this hardcoding for program type
        response_string = CompilerService(RestClient()).run_code(program_code, "python3")
        return response_string