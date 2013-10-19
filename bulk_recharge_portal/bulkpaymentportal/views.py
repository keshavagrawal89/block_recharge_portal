# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import password_reset
from bulkpaymentportal.forms import *
import logging


def main_page(request):

    variables = {
        'head_title':'Welcome to Bulk Recharge Portal',
        'page_title':'Welcome to Bulk Recharge Portal',
        'page_body':'Where you can quickly recharge for all your deserving fans/friends/users',
        'user':request.user
    }
    print request.user
    return render_to_response('main_page.html', RequestContext(request, variables))



def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('Requested user not found!')

    bookmarks = user.bookmarks_set.all()

    variables = {
        'username':username.title(), #doing proper capitalization of the name.
        'bookmarks':bookmarks
    }

    return render_to_response('user_page.html', RequestContext(request, variables))


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    logging.basicConfig(filename='example.log',level=logging.DEBUG,)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        logging.info("*****************I am going to check form validity now***************")
        logging.info("form.is_valid() value: %s" % form.is_valid())
        if form.is_valid():
            logging.info("Form data is valid! Passed values are as follows:")
            logging.info("Username passed: %s" % form.cleaned_data['username'])
            logging.info("Password1 passed: %s" % form.cleaned_data['password1'])
            logging.info("Email passed: %s" % form.cleaned_data['email'])

            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form,
    })

    return render_to_response('registration/register.html', variables)


