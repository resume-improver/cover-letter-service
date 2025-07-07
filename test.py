from get_letter import *

resume_path = 'resume.json'
vacancy_path = 'vacancy.json'
resume = parse_json(resume_path)
vacancy = parse_json(vacancy_path)


letter = get_letter( resume, vacancy )
print(letter)