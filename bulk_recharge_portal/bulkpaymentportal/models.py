from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# This is to keep the account_balance for each user.
class Credits(models.Model):
	user = models.ForeignKey(User)
	account_balance = models.DecimalField(max_digits=5, decimal_places=2)
	# Future account_type column for "PostPaid" or "PrePaid(default)"
	account_type = models.CharField(max_length=8, default="Prepaid")


# This model would serve as a record to store user payment history
class AccountPayment(models.Model):
	user = models.ForeignKey(User)
	previous_balance = models.DecimalField(max_digits=5, decimal_places=2)
	after_balance = models.DecimalField(max_digits=5, decimal_places=2)
	recharge_amount = models.DecimalField(max_digits=5, decimal_places=2)
	date_of_recharge = models.DateTimeField(auto_now_add=True)



class User_account(models.Model):
	user = models.ForeignKey(User)
	# Current balance in the account.
	balance = models.DecimalField(max_digits=5, decimal_places=2)
	# Total number of 'bulk' recharges triggered till date.
	recharges = models.BigIntegerField(max_length=999999999999999)
	# date of bulk recharge triggered.
	date_of_recharge = models.DateField()
	comment = models.CharField(max_length=100)


# This woudl serve as a model to keep record of individual recharges.
class Recharge(models.Model):
	recharged_number = models.BigIntegerField(max_length=999999999999999)
	recharge_value = models.DecimalField(max_digits=5, decimal_places=2)
	date_of_reacharge = models.DateField()
	triggered_by = models.ForeignKey(User)


class Countries(models.Model):
    #   Taking 3 letter ISO code.
    country_iso_code = models.CharField(max_length=3)
    # Some countries have real big name
    country_name = models.CharField(max_length=100)


class PaymentGateways(models.Model):
	name = models.CharField(max_length=100)
	# The value of supported_country would be a csv
	# Example: IND, USA, CAN
	# All these values should match with country_iso_code in countries table.
	supported_country = models.ForeignKey(Countries)


class TelecomNetwork(models.Model):
    # idea is to have a unique combination of country and network like:
    # country 			network
    # USA               AT&T
    # USA               T-Mobile
    # IND               vodafone

	network = models.CharField(max_length=50) # 50 is enough to store
	country = models.ForeignKey(Countries)

class RechargeProviders(models.Model):
	name = models.CharField(max_length=100)
	# Some provioder may fail to provide coverage for a particular
	# network in the same country. So better to have an ID matched
	# with the TelecomNetwork table
	# We may design the model to have data like:
	# X Provider - supported network id(s) - 1,2,3
	# But as of now keeping it this way:
	# X 1
	# X 2
	# Y 1
	# Y 3
	supported_network_id = models.ForeignKey(TelecomNetwork)


class NumberGroups(models.Model):
	user_group_owner = models.ForeignKey(User)
	group_name = models.CharField(max_length=50)
	# In future we can set up a maximum limit restriction on the
	# number of #s which can be stored in the db as a single group
	# for performance issues.
	# Valid data = 1203567890, 918050420391, ...
	saved_numbers = models.TextField()



