A Restful Blog Mangement System

Backend Language
    Python2.7
Web Framework
    Flask
Database
    Sqlite3

TODO:
1. blog、comment
2. user permssion
3. active user
4. change password api
5. change email api
6. blog list optimise
7. image support
8. websockt message

Dev Enviroment Set:
```

pip install requirements.txt
```

Run:
```
python manage.py runserver
```



API:

所有 API 返回 JSON 格式数据

## Blogs

1. list blogs

GET /api/blogs

2. read blog

GET /api/blogs/<id>

3. create blog

POST /api/blogs

Req:

```
{
    "title": "",
    "content": "",
    "category_id": 1
}
```

4. update blog

PUT /api/blogs/<id>

Req:

```
{
    "title": "",
    "content": "",
    "category_id": 1
}
```

可以只传要修改的字段


6. delete blog

DELETE /api/blogs/<id>

## Category

1. List category

GET /api/category

2. Create Category

POST /api/category

req
```
{
    "name": "时事"
}
```

3. Update Category

POST /api/category/<id>

req
```
{
    "name": "时事"
}
```

4. Delete Category

DELETE /api/category/<id>


## Label

1. List labels

GET /api/labels

2. Create Label

POST /api/labels

req
```
{
    "name": "python"
}
```

3. Update Label

POST /api/labels/<id>

req
```
{
    "name": "python"
}
```

4. Delete Label

DELETE /api/labels/<id>


## User

1. List users

GET /api/users

2. Create User

POST /api/users

req
```
{
    "name": "adam", # not required
    "email": "xxxx@xxx.com",
    "password": "123456",
    "gender": 1, # (0, male) (1, female) not required
    "age": 28   # not required
}
```

3. Update User

POST /api/users/<id>

req
```
{
    "name": "adam", # not required
    "gender": 1, # (0, male) (1, female) not required
    "age": 28   # not required
}
```

4. Delete User

DELETE /api/users/<id>




