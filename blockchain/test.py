import requests
import random
import json

response = requests.post(f'http://127.0.0.1:8001/register_node', json={"node_address": "http://127.0.0.1:8002"})
print(response)


response1 = requests.get('http://127.0.0.1:8002/chain')
print(response1)



# # checking connection to the server
# response = requests.get('http://127.0.0.1:5000/')
# print(response.json())

# # GET request to get all the books from the library
# response = requests.get('http://127.0.0.1:5000/books')
# print("\nbooks in the library are:\n", response.json())

# # GET request to get all the visitors in the library
# response = requests.get('http://127.0.0.1:5000/visitors')
# listOfVisitors = response.json()['visitors']

# visitorNames = []
# for i in listOfVisitors:
#     visitorNames.append(i['name'])

# print("\nVisitors of the library are:\n", visitorNames)

# randomVisitor = visitorNames[random.randrange(3)]

# response = requests.get(f"http://127.0.0.1:5000/visitors/{randomVisitor}")
# print(f"\n{randomVisitor} currently has these books:")
# print(response.json()['books_borrowed'])

# # user borrows a book via a POST request, input accepting a json file
# response = requests.post(f'http://127.0.0.1:5000/visitors/{randomVisitor}/borrow', json={'title':'100_recipes'}, auth=('admin','secret'))
# print(f"\n{randomVisitor} has borrowed 100_recipes, here is a summary of all {randomVisitor}\'s books:")
# json_data = json.loads(response.text)
# visitorsBookInfo = json_data['visitor']['borrowed']
# print(visitorsBookInfo)