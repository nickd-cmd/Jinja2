from jinja2 import Template
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
        #add as many of the above elif's for region.  Each region will have it's own template and data file.
        else:
            print("You did not enter a valid hostname. ex: EU-B200-DSW1")
    #Need to make if true for retry
    print("The configuration will be titled 'generated_config.txt' and is located in this directory. \n")
    #create a file for config output.
    config = open("generated_config.txt", "w+")

    #append hostname to file
    config.write("hostname " + hostname + "\n" + "!" + "\n")

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