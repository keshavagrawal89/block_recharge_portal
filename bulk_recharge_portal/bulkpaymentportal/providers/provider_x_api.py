from provider_x import ProviderX

def our_wrapper_recharge_number(number):
	px = ProviderX(developer_key=settings.PROVIDER_X_DEV_KEY)
	'''
		Here we will call separate internal provider_x api methods
		written in provider_x.py
		px.method_1()
		px.method_2()
		...
		do_some_operations()
	'''
	return response
