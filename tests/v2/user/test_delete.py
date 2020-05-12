from requests import delete, get

# некорректные
print(delete('http://localhost:5000/api/v2/users/999').json())
print(delete('http://localhost:5000/api/v2/users/q').json())
print(delete('http://localhost:5000/api/v2/users/').json())

# корректный
print(delete('http://localhost:5000/api/v2/users/1').json())

print(get('http://localhost:5000/api/v2/users').json())
