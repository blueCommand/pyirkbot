# -*- coding: utf-8 -*-

# Plugin created by Merola

import re
import utility
from commands import Command

def random_product_dealextreme(max_price, hardcore):
	max_dollars = utility.currency_conversion(int(max_price), 'sek', 'usd')
	if max_dollars == None:
		return "Oops, something went wrong :("
	
	# Fetch the web page
	response = utility.read_url("http://www.dealextreme.com/products.dx/random.gadgets")
	data = response["data"].replace("\r\n", "")
	#data = data.replace("&nbsp;", "")
	
	product_pattern = "\<a href='\/details.dx\/sku.(\d+)' style=\" font-family: Verdana; font-size: 9pt;\"\>\s+(.+?)\s+\<\/a\>" + \
			".+?" + "style=\"font-size: 11pt;\"\>\s+\$(\d+\.\d\d)\s+\<\/font\>"
	product_iterator = re.finditer(product_pattern, data)
	
	for match in product_iterator:
		if float(match.group(3)) <= max_dollars:
			if hardcore:
				return "Gogogo! http://www.dealextreme.com/shoppingcart.dx/add." + match.group(1) + "~quantity.1#_ctl0_content_pCheckout"
			else:
				return "$" + match.group(3) + ": " + match.group(2) + " | http://www.dealextreme.com/details.dx/sku." + match.group(1)
	
	return "No suitable product found :("

class RandomBuyCommand(Command):
	usage = "Work in progress! Usage: .buy dx <max price in sek> | .buy dx! <max price in sek>"
	
	def __init__(self):
		pass
		
	def trig_buy(self, bot, source, target, trigger, argument):
		"""Work in progress!"""
		
		# Sanitize argument
		argument = argument.strip()
		args = argument.split(' ', 1)
		
		# Show usage
		if (not args[0]) or (len(args) < 2):
			return self.usage
		
		# Ensure max price is a number
		elif not args[1].isdigit():
			return "That is not a number :("
				
		# dealextreme.com
		elif args[0].lower() == 'dx':
			return random_product_dealextreme(args[1], False)
				
		# dealextreme.com, hardcore mode
		elif args[0].lower() == 'dx!':
			return random_product_dealextreme(args[1], True)
		
		# Unknown subcommand
		else:
			return "Unknown source! " + self.usage