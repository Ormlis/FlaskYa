from requests import post, get

# пустой запрос
print(post('http://localhost:5000/api/v2/jobs').json())

# запрос с одним параметром
print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'Job'}).json())

# корректный запрос
print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'Job',
                 'team_leader': 1,
                 'work_size': 1,
                 'collaborators': '1, 2, 3',
                 'start_date': '2020-01-01',
                 'end_date': '2020-06-01',
                 'is_finished': False}).json())

print(get('http://localhost:5000/api/v2/jobs').json())
