from requests import get

# все работы
print(get('http://localhost:5000/api/jobs').json())

# одна работа
print(get('http://localhost:5000/api/jobs/1').json())

# неверный id
print(get('http://localhost:5000/api/jobs/999').json())

# неверный тип айди (строка)
print(get('http://localhost:5000/api/jobs/q').json())
