postgres:
	docker run --name blog-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=1111 -e POSTGRES_DB=blog-db -p 5432:5432 -d postgres:latest

runserver:
	cd ./app && uvicorn main:app --reload

makemigrations:
	cd ./app && alembic revision --autogenerate

migrate:
	cd ./app && alembic upgrade head
