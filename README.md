# FastAPIBlog

## Summary

A simple API simulating a blog done with Python and FastAPI framework.\
The project doesn't serve much purpose, it's just for learning.
Detailed documentation provided by `Swagger` is available by going `/docs` path.
<br>

## Installation

Create virtual environment (Ubuntu):
```shell
$ python3 -m venv env
```
<br>

Start using virtual environment:

```shell
$ source env/bin/activate
```
<br>

Install required packages:

```shell
(env) $ pip install -r requirements.txt
```
<br>

## Running application

To initiate database:
```shell
(env) $ make postgres
```
<br>

To create migrations:
```shell
(env) $ make makemigrations
```
<br>

To migrate:
```shell
(env) $ make migrate
```
<br>

To run `uvicorn` server:
```shell
(env) $ make runserver
```
<br>

> If you encounter any issues, check out "Possible issues" section.

## Possible issues

<details><summary>Show list of possible issues and their solutions</summary>
<br>

If port `:5432` is already occupied:
```shell
(env) $ sudo lsof -i :5432
(env) $ sudo kill <process_id>
```
<br>

If container already exists:
```shell
(env) $ docker ps -a
(env) $ docker rm <container_id>
```
</details>

