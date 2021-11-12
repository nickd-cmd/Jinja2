#ip function
import ipaddress

def validate_mgmt(address):
    try:
        ip = ipaddress.ip_address(address)
        print("Valid".format(address, ip))
    except ValueError:
        print("Not Valid".format(address))

mgmt_ip = input("enter the ip: ")
validate_mgmt(mgmt_ip)