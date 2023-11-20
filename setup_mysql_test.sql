-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- Create or update the hbnb_test user with the required privileges
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Grant all privileges on the hbnb_test_db database to the hbnb_test user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- Grant SELECT PRIVILEGE ON THE performance_schema database to the hbnb_test_db
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
