CREATE USER vbv WITH PASSWORD 'vbv';
CREATE DATABASE vbvdb;
GRANT ALL PRIVILEGES ON DATABASE vbvdb TO vbv;

\connect vbvdb;

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO employees (name, position, salary) VALUES
('Bhuvi', 'Manager', 675000.00),
('Vibhu', 'Developer', 555000.00),
('Rudra', 'Analyst', 460000.00);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO vbv;