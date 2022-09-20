COMMAND='
CREATE DATABASE db;
USE db;
CREATE TABLE students (name VARCHAR(255), age INT);
INSERT students (name, age) VALUES ("Taro", 16), ("Hanako", 17), ("Pochi", 3);'

mysql --user=root --password=my-password --execute="$COMMAND"