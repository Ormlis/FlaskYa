from requests import get

# все работы
print(get('http://localhost:5000/api/v2/jobs').json())

# одна работа
print(get('http://localhost:5000/api/v2/jobs/1').json())

# неверный id
print(get('http://localhost:5000/api/v2/jobs/999').json())

# неверный тип айди (строка)
print(get('http://localhost:5000/api/v2/jobs/q').json())
