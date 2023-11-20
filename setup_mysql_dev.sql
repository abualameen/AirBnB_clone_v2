-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create or update the hbnb_dev user with the required privileges
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant all privileges on the hbnb_dev_db database to the hbnb_dev user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Grant SELECT PRIVILEGE ON THE performance_schema database to the hbnb_dev_db
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
