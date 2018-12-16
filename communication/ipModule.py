#############
# IP Module #
#############

"""This module can be used to validate the format of an IP address."""

def validate_ip_4(ip_addr):
	"""Function to validate an IPV4 format in 4 decimals and noport added.""" 
	ip_addr_split = ip_addr.split(".")
	if len(ip_addr_split) != 4:
		return False
	for x in ip_addr_split:
		if not x.isdigit():
			return False
		i = int(x)
		if i < 0 or i > 255:
			return False
	return True
