from jinja2 import Template
import is_ipv4
import yaml

def main():
    #Set our hostname variable and pull from it to determine region files
    for retry in range(3):
        hostname = input("Enter the hostname of the device you want to configure: ") #re-use the hostname string for line 1 of config
        region = hostname[0:2]
        if region == "EU":
            print("Making an EU specific configuration:")
            #open the template
            x = open("eu_template.j2")
            template = x.read()
            #open the appropriate yaml file
            with open('eu_data.yml') as y:
                region_data = yaml.full_load(y)
            break
        elif region == "SE":
            print("Making a SE specific configuration:")
            x = open("se_template.j2")
            template = x.read()
            with open('se_data.yml') as y:
                region_data = yaml.full_load(y)
            break
        #add regions as needed.  Each region will have it's own template and data file.
        else:
            print("\nYou did not enter a valid hostname. ex: EU-BLDG10-DSW01\n")
            if retry == int(2): #exits out of the program after 3 failed attempts
                exit() 

    mgmt_vlan = input("Management Vlan (ex.100): ")

    verify_ip = False
    while not verify_ip:
        mgmt_ip = input("Enter the management IP address: ")
        verify_ip = is_ipv4.is_ipv4_address(mgmt_ip)
    
    verify_sub = False
    while not verify_sub:
        mgmt_sub = input("Enter the management subnet: ")
        verify_sub = is_ipv4.is_ipv4_address(mgmt_sub)
    
    print("The configuration will be titled 'generated_config.txt' and is located in this directory. \n")
    #create a file for config output.
    config = open("generated_config.txt", "w+")

    #append hostname to file
    config.write("hostname " + hostname + "\n" + "!" + "\n")

    #append mgmgt vlan and ip to file
    config.write("vlan " + mgmt_vlan + "\n" + "ip address " + mgmt_ip + " " + mgmt_sub + "\n" + "exit \n!\n")

    #append region specific config to file
    j2_template = Template(template)
    config.write(j2_template.render(region_data))

    #append enterprise config to file
    with open ("enterprise_template.j2") as e:
        entTemplate = e.read()

    with open ("ent_data.yml") as z:
        ent_data = yaml.full_load(z)

    ent_j2_template = Template(entTemplate)
    config.write(ent_j2_template.render(ent_data))

if __name__ == "__main__":
    main()
