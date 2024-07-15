# practice FastAPI(베타리딩)

> 제이펍에서 출간될 FastAPI 베타리딩을 하는 과정에서 작성한 코드 입니다.

## 설정

- 책에서는 `poetry`를 사용법이 잘 나와있음
    - Ubuntu 24.04 사용자는 [miniconda](https://docs.anaconda.com/miniconda/)를 사용
    - Ubuntu 24.04와 몇가지 충돌이 발생하기 때문에 conda 환경에서 GCC 등을 설정
        - `conda install -c conda-forge gcc=12.1.0`

```bash
$ sudo apt install python3-dev default-libmysqlclient-dev pkg-config
(practice-fastapi)  $ pip install fastapi
(practice-fastapi)  $ pip install 'uvicorn[standard]'
(practice-fastapi)  $ pip install py-ulid
(practice-fastapi)  $ pip install 'passlib[bcrypt]'
(practice-fastapi)  $ pip install sqlalchemy mysqlclient alembic
(practice-fastapi)  $ pip install dependency-injector
(practice-fastapi)  $ pip freeze > requirements.txt
```

## DB 설정

- 개인적으로 PostgreSQL을 사용하고 있어서, MySQL은 Docker를 사용해서 실습을 진행

```bash
$ docker run --name mysql-fastapi -p 3306:3306 -e MYSQL_ROOT_PASSWORD=qwer1234 -d mysql:8
Unable to find image 'mysql:8' locally
8: Pulling from library/mysql
7af76bb36546: Pull complete 
e9fcbbd95294: Pull complete 
edbdb6512ec5: Pull complete 
8bde54dd677d: Pull complete 
16c32d19d44f: Pull complete 
b77457e95149: Pull complete 
c3f71f60365b: Pull complete 
78a657cda140: Pull complete 
44fc47757fc5: Pull complete 
0035d4d93c34: Pull complete 
Digest: sha256:d26a69e1ef146c77ecfddf3128134e3a0f4c6123133725835818107037649827
Status: Downloaded newer image for mysql:8
18cd8054b0e7956967d2cdd39cfd343cfce60f7a9e02f4023d9c378791532af1
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                                  NAMES
18cd8054b0e7   mysql:8   "docker-entrypoint.s…"   24 seconds ago   Up 23 seconds   0.0.0.0:3306->3306/tcp, :::3306->3306/tcp, 33060/tcp   mysql-fastapi
$ docker exec -it 18cd8054b0e7 bash
bash-5.1# mysql -u root -p
mysql> SHOW DATABASE;
mysql> CREATE SCHEMA `fastapi-ca`;
```

## 실행

```bash
$ alembic upgrade head
$ python main.app
```

### curl 모음

- 1

```bash
$ curl -X GET http://localhost:8000 | jq
```

- 2

```bash
$ curl -X 'POST' \
'http://localhost:8000/users' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
  "name": "sd",
  "email": "sd@app.com",
  "password": "qwer1234"
}'
```

- 3

```bash
$ curl -X 'PUT' \
'http://localhost:8000/users/01J2PK2VZEXWZD3DTNWMN0QKQ9' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
  "name": "sd(1)"
}'
```

- 4

```bash
$ curl -X 'GET' 'http://localhost:8000/users'
```

- 5

```bash
$ curl -X 'GET' 'http://localhost:8000/users?page=2&items_per_page=3'
```

- 6

```bash
$ curl -X 'DELETE' 'http://localhost:8000/users?user_id=UserID-02'
```

- 7

```bash
$ curl -X 'POST' \
'http://localhost:8000/users' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
  "name": "sd",
  "email": "sd",
  "password": "qwer1234"
}'
```

- 8

```bash
$ curl -X 'POST' \
'http://localhost:8000/users/login' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'username=sd%40app.com&password=qwer1234'
```