from requests import put, get

# пустой запрос
print(put('http://localhost:5000/api/jobs/1').json())

# запрос с неккоректным айди
print(put('http://localhost:5000/api/jobs/213321',
          json={'job': 'Job',
                'team_leader': 1,
                'work_size': 23,
                'collaborators': '1, 2, 3',
                'start_date': '01-01-2020',
                'end_date': '01-06-2020',
                'is_finished': False}).json())

# корректный запрос
print(put('http://localhost:5000/api/jobs/2',
          json={'job': 'Job22',
                'team_leader': 1,
                'work_size': 13,
                'collaborators': '1, 2, 3',
                'start_date': '2020-02-01',
                'end_date': '2020-06-01',
                'is_finished': False}).json())

print(get('http://localhost:5000/api/jobs').json())
