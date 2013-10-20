class ProviderY(object):
	def __init__(self, developer_key=""):
		self._dev_key = developer_key
		self._debug = debug

	def recharge_number(self, number, operator):
		'''
			This guy suppose returns XML response
			So we will have to deal with XML parser.
			If suppose 'result' is the response from their API then
		'''
		some_dictionary = xmlparser(result)
		....
		return some_dictionary # This dictionary will be read by our custom wrapper provider_y_api.py

	def get_operator(self, number):
		....


if __name__ == "__main__":
	providery = ProviderY(developer_key="xh2361vhHdh273hjdbhvU&AJ878") # some random key
