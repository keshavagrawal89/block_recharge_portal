from provider_y import ProviderY

def our_wrapper_recharge_number(number):
	py = ProviderY(developer_key=settings.PROVIDER_Y_DEV_KEY)
	'''
		Here we will call separate internal provider_y api methods
		written in provider_y.py
		py.method_1()
		returned_dictionary = py.method_2(params)
		...
		do_some_operations(returned_dictionary)
	'''
	return response
