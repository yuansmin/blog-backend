A Restful Blog Mangement System

Backend Language
    Python2.7
Web Framework
    Flask
Database
    Sqlite3

Dev Enviroment Set:
```
pip install -r requirements.txt
```

Init Datebase
```shell
python manage.py db init  # use sqlite3 Default 
```

Apply Mode change to database
```
python manage.py db migrate
python manage.py db upgrade

```

Run:
```
python manage.py runserver  # running on 127.0.0.1:5000 Default  
```

TODO:
-[x] blog、comment
-[x] config db, port
-[ ] user permssion
-[ ] active user
-[x] change password api
-[ ] change email api
-[ ] blog list optimise
-[ ] image support
-[ ] websockt message


API:

所有 API 返回 JSON 格式数据

错误时返回 `{"message": "", "code": 500}`

## Blogs

1. list blogs

GET /api/blogs

Query Parameters

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------ | ---     | ---     |
| limit | int | false  | 20      | items per-page |
| offset| int | false  | 0       | |

Response: 200

```
{
    "items": [
        {
            "title": "",
            "content": "",
            "category_id": 1,
            "user_id": ,
            "create_time": "2018-01-30 09:10:11",
            "published_time": "xx", # maybe null
            "view_count": 0,
            "good_count": 0 
        }
    ]
}
```


2. read blog

GET /api/blogs/<id>

Path Parameters

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------ | ---     | ---     |
| id   | int  |  true  |  -      | blog id |


Response 200
```
{
    "title": "",
    "content": "",
    "category_id": 1,
    "user_id": ,
    "create_time": "2018-01-30 09:10:11",
    "published_time": "xx", # maybe null
    "view_count": 0,
    "good_count": 0 
}
```

3. create blog

POST /api/blogs

Body Parameters

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------ | ---     | ---     |
| title| string| true  | -       |blog title |
|content| string| true | -       | |
|category_id| int| true | -       | |

Req:

```
{
    "title": "",
    "content": "",
    "category_id": 1
}
```

Response: 201

```
{
    "title": "",
    "content": "",
    "category_id": 1,
    "user_id": ,
    "create_time": "2018-01-30 09:10:11",
    "published_time": "xx", # maybe null
    "view_count": 0,
    "good_count": 0 
}
```



4. update blog

POST /api/blogs/<id>

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------ | ---     | ---     |
| title| string| false  | -       |blog title |
|content| string| false | -       | |
|category_id| int| false | -       | |

可以只传要修改的字段

Req:

```
{
    "title": "",
    "content": "",
    "category_id": 1
}
```

Response 200

```
{
    "title": "",
    "content": "",
    "category_id": 1,
    "user_id": ,
    "create_time": "2018-01-30 09:10:11",
    "published_time": "xx", # maybe null
    "view_count": 0,
    "good_count": 0 
}
```


6. delete blog

DELETE /api/blogs/<id>

Path Parameters

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------ | ---     | ---     |
| id   | int  |  true  |  -      | blog id |

Response 200


## Category

1. List category

GET /api/category

Response 200

```
{
    "items": [
        {
            "id": 1,
            "name": "技术",
            "user_id": 1,
            "create_time": "2018-01-30 09:10:11"
        }
    ]
}
```


2. Create Category

POST /api/category

Body Parameters

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------  | ---     | ---     |
|name  |string|true     | -       | categroy name|

Request

```
{
    "name": "技术"
}
```

Response 201

```
{
    "id": 1,
    "name": "技术",
    "user_id": 1,
    "create_time": "2018-01-30 09:10:11"
}
```


3. Update Category

I don't think it's a good idea to update the category


4. Delete Category

DELETE /api/category/<id>

Path Parameters

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------  | ---     | ---     |
|id    | int  |true     | -       | category id |


## Label

1. List labels

GET /api/labels

Response 200

```
{
    "items": [
        {
            "id": 1,
            "name": "python",
            "user_id": 1,
            "create_time": "2018-01-30 09:10:11"
        }
    ]
}
```


2. Create Label

POST /api/labels

Body Parameters

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------  | ---     | ---     |
|name  |string|true     | -       | label name|

req
```
{
    "name": "python"
}
```

Response 201

```
{
    "id": 1,
    "name": "python",
    "user_id": 1,
    "create_time": "2018-01-30 09:10:11"
}
```

4. Delete Label

DELETE /api/labels/<id>

Path Parameters

| Name | Type |Required | Default  | Description |
| ---- | ---  | ------  | ---     | ---     |
|id    | int  |true     | -       | label id |


## User

1. List users

GET /api/users

2. Create User

POST /api/users

req
```
{
    "name": "adam", # not Required 
    "email": "xxxx@xxx.com",
    "password": "123456",
    "gender": 1, # (0, male) (1, female) not Required 
    "age": 28   # not Required 
}
```

3. Update User

POST /api/users/<id>

req
```
{
    "name": "adam", # not Required 
    "gender": 1, # (0, male) (1, female) not Required 
    "age": 28   # not Required 
}
```

4. Delete User

DELETE /api/users/<id>

5. Login

POST /api/users/login

req：
```json
{
  "email": "xxxxx",
  "password": "xxx"
}
```

6. Logout

GET /api/users/logout




