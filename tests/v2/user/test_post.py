from requests import post, get

# пустой запрос
print(post('http://localhost:5000/api/v2/users').json())

# запрос с одним параметром
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Jack'}).json())

# корректный запрос
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Jack',
                 'surname': 'Chris',
                 'age': 12,
                 'position': 'first',
                 'speciality': 'second',
                 'address': 'here',
                 'email': 'new_email@email.com',
                 'city_from': 'Барнаул'}).json())

print(get('http://localhost:5000/api/v2/users').json())
