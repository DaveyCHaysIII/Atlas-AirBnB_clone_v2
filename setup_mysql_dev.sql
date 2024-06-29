-- this is a script to set up the dev user
-- script to run: mysql -u root -p < setup_mysql_dev.sql
-- note: mysql has to be running for this script to function
-- you can start mysql by running sudo service mysql start
-- and check server status with sudo service mysql status
-- enter the client with mysql -u hbnb_dev -p

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';