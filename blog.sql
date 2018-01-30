create table blogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200),
    content TEXT,
    user_id INTEGER,
    created_time VARCHAR(50),
    published_time VARCHAR(50),
    category_id INTEGER,
    view_count INTEGER,
    good_count INTEGER
);

create table users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200),
    age INTEGER,
    gender TINYINT,
    email VARCHAR(200),
    password VARCHAR(500),
    phone_number VARCHAR(50),
    sign_up_time VARCHAR(50),
    last_login_time VARCHAR(50)
);

create table labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200)
);

create table blog_label (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blog_id INTEGER,
    label id INTEGER
);

create table category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200)
);