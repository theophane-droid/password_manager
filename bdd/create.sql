drop table if exists password;
drop table if exists user;

create table user(
    name varchar(200) primary key,
    passwd varchar(200)
);

create table password(
    id integer primary key,
    pname text,
    content text,
    user_name varchar(200),
    foreign key (user_name) references user(id_user)
);
