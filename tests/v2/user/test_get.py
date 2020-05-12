from requests import get

# все пользователи
print(get('http://localhost:5000/api/v2/users').json())

# один пользователь
print(get('http://localhost:5000/api/v2/users/1').json())

# неверный id
print(get('http://localhost:5000/api/v2/users/123512').json())

# неверный тип айди (строка)
print(get('http://localhost:5000/api/v2/users/q').json())
