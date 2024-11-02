import json

with open('intermediate_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

count = len(data)
print("Number of objects:", count)

