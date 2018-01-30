Backend Language
    Python2.7
Web Framework
    Tornado
Database
    Sqlite3

DB Model
    1. blog
        create table blog (
            id INTEGER primary key auto increament,
            title VARCHAR(200),
            content TEXT,
            author_id INTEGER,
            created_time VARCHAR(50),
            published_time VARCHAR(50),
            category_id INTEGER
        );

    2. author
        create table author (
            id INTEGER primary key auto increament,
            name VARCHAR(200),
            age TINYINT,
            gender INTEGER,
            email VARCHAR(200),
            phone_number VARCHAR(50),
            sign_up_time VARCHAR(50)
        );

    3. label
        create table label (
            id INTEGER primary key auto increament,
            name VARCHAR(200)
        );

    4. blog_label
        create table blog_label (
            id INTEGER primary key auto increament,
            blog_id INTEGER,
            label id INTEGER
        );

    5. category
        create table category (
            id INTEGER primary key auto increament,
            name VARCHAR(200)
        );


API:

1. list blogs
    GET /api/blogs

2. read blog
    GET /api/blogs/<id>

3. create blog
    POST /api/blogs
    Req:
        {
            "title": "",
            "content": "",
            ...
        }

4. replace blog
    PUT /api/blogs/<id>
    Req:
        {
            "title": "",
            "content": "",
            ...
        }

5. patch blog
    PATCH /api/blogs/<id>
    Req:
        {
            "":""
        }

6. delete blog
    DELETE /api/blogs/<id>


