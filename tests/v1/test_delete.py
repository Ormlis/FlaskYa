from requests import delete, get

# некорректные
print(delete('http://localhost:5000/api/jobs/999').json())
print(delete('http://localhost:5000/api/jobs/q').json())
print(delete('http://localhost:5000/api/jobs/').json())

# корректный
print(delete('http://localhost:5000/api/jobs/1').json())

print(get('http://localhost:5000/api/jobs').json())
