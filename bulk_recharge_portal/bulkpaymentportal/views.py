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
from bulkpaymentportal.models import *
import logging
import uuid
import csv
import datetime
import stripe

def main_page(request):

    variables = {
        'head_title':'Welcome to Bulk Recharge Portal',
        'page_title':'Welcome to Bulk Recharge Portal',
        'page_body':'Where you can quickly recharge for all your deserving fans/friends/users',
        'user':request.user
    }
    print request.user
    return render_to_response('main_page.html', RequestContext(request, variables))


# Will be used as to prepare dashboard
def user_page(request):
#    try:
#        user = User.objects.get(username=username)
#    except:
#        raise Http404('Requested user not found!')

#    balance = user_account.objects.get('balance')

    variables = {
 #       'username':username.title(), #doing proper capitalization of the name.
 #       'balance': balance
    }

    return render_to_response('dashboard.html', RequestContext(request, variables))


def charge_customer():
	# dummy key
	stripe.api_key = "sk_test_mkGsLqEW6SLnZa487HYfJVLf"

	token = request.POST.get('stripeToken')
	r_amount = request.POST.get('amount')
	user_ = request.POST.get('user_')

	try:
	  charge = stripe.Charge.create(
    	  amount = r_amount,
	      currency = "usd",
    	  card = token,
	      description = "xyz@syz.com"
	  )
	  logging.info("Charge created: %s" % str(charge))

	  update_payment_history(user_, r_amount)
	  update_account_balance(user_, r_amount, "add")

	except stripe.CardError, e:
	  # The card has been declined
	  logging.error("The card has been declined: %s" % e)



def update_account_balance(user_, r_amount, operation):
	r_amount = decimal.Decimal(r_amount)

	user_current_balance = Credits.objects.values_list('account_balance', flat=True).filter(user=User.objects.get(username = user_))[0]

	if operation == "add":
		# If this is a first recharge. Right now by default account balance
		# is not 0 and so the check...
		if user_current_balance == None or user_current_balance == 0:
			affected_row = Credits.objects.filter(user = User.objects.get(username = user_)).update(account_balance=r_amount)
			if affected_row == 1:
				logging.info("Account balance updated: %s" % r_amount)
			else:
				logging.error("Something got messed up!")
		else:
			affected_row = Credits.filter(user = User.objects.get(username = user_)).update(account_balance=r_amount + user_current_balance)
            if affected_row == 1:
                logging.info("Account balance updated: %s" % r_amount)
            else:
                logging.error("Something got messed up!")

	elif operation == "deduct":
        if user_current_balance == None or user_current_balance == 0:
			r_amount = -r_amount
            affected_row = Credits.filter(user = User.objects.get(username = user_))\
							.update(account_balance=r_amount)
            if affected_row == 1:
                logging.info("Account balance updated: %s" % r_amount)
            else:
                logging.error("Something got messed up!")
        else:
            affected_row = Credits.filter(user = User.objects.get(username = user_))\
							.update(account_balance=r_amount - user_current_balance)
            if affected_row == 1:
                logging.info("Account balance updated: %s" % r_amount)
            else:
                logging.error("Something got messed up!")

def update_payment_history(user_, r_amount):
	previous_balance = Credits.objects.values_list('account_balance', flat=True)\
						.filter(user=User.objects.get(username=user_))[0]
	try:
		account_payment = AccountPayment(user = User.objects.get(username=user_),\
							 previous_balance=previous_balance, \
							after_balance=decimal.Decimal(r_amount + previous_balance), \
							recharge_amount=r_amount)
		account_payment.save()
	except Exception, e:
		logging.error("Woh! Something got screwed!")
		system.exit(1)
'''
 id | user_id | previous_balance | after_balance | recharge_amount |       date_of_recharge        
----+---------+------------------+---------------+-----------------+-------------------------------
  1 |       2 |             0.00 |        100.00 |          100.00 | 2013-10-20 03:22:11.858189+00

'''


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



def forgot_password(request):
    variables = {}
    if request.method == 'POST':
        return password_reset(request, from_email = request.POST.get('email'))
    else:
        return  render_to_response('registration/forgot_password.html', RequestContext(request, variables))


def manage_groups(request):
    if request.method == 'POST':
        if (request.FILES['grp-numbers-file'] and request.POST.get('grp-text')):
            name = request.POST.get('grp-text')
            user_ = request.POST.get('user_')

            # save the file from django in-memory to some path
            to_be_read = save_file(request.FILES['grp-numbers-file'])

            # Now reading the file
            number_list = read_file(to_be_read)

            # save the numbers in the db
            save_in_db(number_list, name, user_)

            user_groups = NumberGroups.objects.values_list('group_name', flat=True).filter(user_group_owner=User.objects.get(username=user_))
            variables = {
                'user_groups': user_groups,
            }

        return render_to_response('groups.html', RequestContext(request, variables))


def show_groups(request):
	if request.method == 'POST':
			print "I am here"
			user_ = request.POST.get('user_')
			print user_
			user_groups = NumberGroups.objects.values_list('group_name', flat=True).filter(user_group_owner=User.objects.get(username=user_))
			print user_groups
			variables = {
				'user_groups': user_groups,
			}
	return render_to_response('groups.html', RequestContext(request, variables))


def save_file(f):
	print "I am in save_file"
	tmp_file_name = 'userfile%s.csv' % uuid.uuid4()
	file_path = 'tmp/%s' % tmp_file_name
	with open(file_path, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	return tmp_file_name


def read_file(f):
	file_path = 'tmp/%s' % f
	with open(file_path, 'rb') as csvfile:
		grp_numbers = csv.reader(csvfile)
		group_numbers = ""
		for line in grp_numbers:
			grp_number = ",".join(str(ele) for ele in line)
			group_numbers = group_numbers + "," + str(grp_number)
			
		return group_numbers.strip(',')


def save_in_db(number_list, name, user_):
	grp_number = NumberGroups(user_group_owner=User.objects.get(username=user_), group_name=name, saved_numbers=number_list)
	grp_number.save()
