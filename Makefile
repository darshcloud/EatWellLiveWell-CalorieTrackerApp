build:
	docker build -t calorietracker .
run:
	docker run -p 8000:8000 -v ~/.env:/calorietracker/.env --env-file .env calorietracker
run_l:
	python3 manage.py runserver