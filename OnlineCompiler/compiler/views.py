from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator

from .forms import ProgramInputForm

@login_required(login_url="/login/")
def run_program(request):
    print("Got the request to run code"+str(request))
    if request.method == 'GET':
        context={"form":ProgramInputForm}
        return render(request, 'CodeInput.html', context=context)
    else:
        response_string = ProgramInputForm().run_program(request)
        return HttpResponse(response_string)