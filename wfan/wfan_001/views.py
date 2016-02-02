from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
#from slapp.models import Choice, Poll

def index(request):
    return HttpResponse("Hello, world.")
