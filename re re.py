from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

def normalize_name(name):
    parts = name.split()
    if len(parts) == 3:
        return parts
    elif len(parts) == 2:
        return parts + ['']
    elif len(parts) == 1:
        return parts + ['', '']
    return ['', '', '']

def normalize_phone(phone):
    phone_pattern = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})(\s*доб\.\s*(\d+))?')
    match = phone_pattern.search(phone)
    if match:
        formatted_phone = f'+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}'
        if match.group(7):
            formatted_phone += f' доб.{match.group(7)}'
        return formatted_phone
    return phone

normalized_contacts = []
header = contacts_list[0]
contacts_list = contacts_list[1:]

for contact in contacts_list:
    lastname, firstname, surname = normalize_name(contact[0] + " " + contact[1] + " " + contact[2])
    organization = contact[3]
    position = contact[4]
    phone = normalize_phone(contact[5])
    email = contact[6]
    normalized_contacts.append([lastname, firstname, surname, organization, position, phone, email])

contacts_dict = {}
for contact in normalized_contacts:
    key = (contact[0], contact[1])
    if key in contacts_dict:
        for i in range(len(contact)):
            if contact[i]:
                contacts_dict[key][i] = contact[i]
    else:
        contacts_dict[key] = contact

result_contacts = [header] + list(contacts_dict.values())

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawrite = csv.writer(f, delimiter=",")
    datawrite.writerows(result_contacts)

pprint(result_contacts)
