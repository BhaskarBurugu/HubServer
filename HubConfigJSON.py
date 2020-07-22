import json

person_dict = {
                "HubCat": "FPGA"
              }

with open('HubCat.JSON', 'w') as json_file:
  json.dump(person_dict, json_file)


with open('HubCat.JSON') as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(type(data))
print(data["HubCat"])