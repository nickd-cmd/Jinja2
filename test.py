from jinja2 import Template
import yaml

x = open("enterprise_template.j2")
template = x.read()

with open('test_data.yml') as y:
    data = yaml.load(y)

for key, value in data.items():
    j2_template = Template(template)
    data[key] = j2_template.render(**data)

print(j2_template.render(data))