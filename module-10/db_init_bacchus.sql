/*
    Title: db_init_bacchus.sql
    Date: 10 July 2024
    Description: Bacchus database initialization script.
*/

-- drop database user if exists 
DROP USER IF EXISTS 'taste_user'@'localhost';

-- create taste_user and grant them all privileges to the Bacchus database 
CREATE USER 'taste_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'wine';

-- grant all privileges to the Bacchus database to user taste_user on localhost 
GRANT ALL PRIVILEGES ON Bacchus.* TO 'taste_user'@'localhost';

-- grant all privileges to the Bacchus database to user taste_user on localhost 
GRANT ALL PRIVILEGES ON Bacchus.* TO 'taste_user'@'localhost';


-- drop tables if they are present
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS deliveries;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS wine;
DROP TABLE IF EXISTS supplier;

-- create the wine distribution table
CREATE TABLE wine (
    wine_id     INT             NOT NULL        AUTO_INCREMENT,
    wine_type   VARCHAR(75)     NOT NULL,
    PRIMARY KEY(wine_id)
); 

-- create the supplier table
CREATE TABLE supplier (
    supplier_id     INT             NOT NULL        AUTO_INCREMENT,
    supplier_name   VARCHAR(75)     NOT NULL,
    supply_type     VARCHAR(75)     NOT NULL,
    PRIMARY KEY(supplier_id)
);

-- create the inventory table
CREATE TABLE inventory (
    inventory_id    INT            NOT NULL        AUTO_INCREMENT,
    quantity        INT            NOT NULL,
    supply_type     VARCHAR(75)    NOT NULL,
    supplier_id     INT            NOT NULL,
    PRIMARY KEY(inventory_id),
    CONSTRAINT fk_supplier_inventory
    FOREIGN KEY(supplier_id)
        REFERENCES supplier(supplier_id)
);

-- create the deliveries table 
CREATE TABLE deliveries (
    delivery_id     INT             NOT NULL        AUTO_INCREMENT,
    supplier_id     INT             NOT NULL,
    delivery_name   VARCHAR(75)     NOT NULL,
    expected_date   DATE            NOT NULL,
    actual_date     DATE            NOT NULL,
    PRIMARY KEY(delivery_id),
    CONSTRAINT fk_supplier_delivery
    FOREIGN KEY(supplier_id)
        REFERENCES supplier(supplier_id)
); 

-- create the orders table
CREATE TABLE orders (
    orders_id        INT             NOT NULL        AUTO_INCREMENT,
    inventory_id     INT             NOT NULL,
    supplier_id      INT             NOT NULL,
    order_date       DATE            NOT NULL,
    delivery_id      INT             NOT NULL,
    wine_id          INT             NOT NULL,
    PRIMARY KEY(orders_id),
    CONSTRAINT fk_inventory_order
    FOREIGN KEY(inventory_id)
        REFERENCES inventory(inventory_id),
    CONSTRAINT fk_supplier_order
    FOREIGN KEY(supplier_id)
        REFERENCES supplier(supplier_id),
    CONSTRAINT fk_delivery_order
    FOREIGN KEY(delivery_id)
        REFERENCES deliveries(delivery_id),
    CONSTRAINT fk_wine_order
    FOREIGN KEY(wine_id)
        REFERENCES wine(wine_id)
);

-- create the employee table
CREATE TABLE employee (
    employee_id        INT             NOT NULL        AUTO_INCREMENT,
    employee_firstname VARCHAR(75)     NOT NULL,
    employee_lastname  VARCHAR(75)     NOT NULL,
    employee_hours     INT             NOT NULL,
    employee_position  VARCHAR(75)     NOT NULL,
    PRIMARY KEY(employee_id)
);

-- create the department table and set the foreign key
CREATE TABLE department (
    department_id       INT             NOT NULL        AUTO_INCREMENT,
    department_name     VARCHAR(75)     NOT NULL,
    employee_id         INT             NOT NULL,
    PRIMARY KEY(department_id),
    CONSTRAINT fk_employee_department
    FOREIGN KEY(employee_id)
        REFERENCES employee(employee_id)
);

-- insert wine records
INSERT INTO wine (wine_id, wine_type) VALUES
    (12096, 'Merlot'),
    (12097, 'Cabernet'),
    (12098, 'Chablis'),
    (12099, 'Chardonnay');

-- insert supplier records
INSERT INTO supplier (supplier_id, supplier_name, supply_type) VALUES
    (12134, 'Supplier 1', 'Bottles and Corks'),
    (12133, 'Supplier 2', 'Labels and Boxes'),
    (12135, 'Supplier 3', 'Vats and Tubing');

-- insert inventory records
INSERT INTO inventory (inventory_id, quantity, supply_type, supplier_id) VALUES
    (12647, 1425, 'Bottles and Corks', 12134),
    (12643, 1263, 'Labels and Boxes', 12133),
    (12645, 1687, 'Vats and Tubing', 12135);

-- insert delivery records
INSERT INTO deliveries (delivery_id, supplier_id, delivery_name, expected_date, actual_date) VALUES
    (30029, 12134, 'Black', '2024-09-15', '2024-09-13'),
    (30027, 12133, 'Smith', '2024-10-07', '2024-10-10'),
    (30016, 12135, 'Permudez', '2024-08-22', '2024-08-23'),
    (30035, 12134, 'Jimenez', '2024-08-23', '2024-08-19'),
    (30084, 12135, 'April', '2024-08-19', '2024-08-09'),
    (30054, 12134, 'Lund', '2024-09-05', '2024-09-05');

-- insert orders records
INSERT INTO orders (orders_id, inventory_id, supplier_id, order_date, delivery_id, wine_id) VALUES
    (00931, 12647, 12134, '2024-08-31', 30029, 12096),
    (00935, 12643, 12133, '2024-09-30', 30027, 12097),
    (00939, 12645, 12135, '2024-08-19', 30016, 12098),
    (00937, 12647, 12133, '2024-08-12', 30027, 12099),
    (00936, 12647, 12135, '2024-08-04', 30029, 12096),
    (00932, 12643, 12134, '2024-08-31', 30029, 12097);

-- insert employee records
INSERT INTO employee (employee_id, employee_position, employee_hours, employee_firstname, employee_lastname) VALUES
    (24, 'Accounting Lead', 40, 'Janet', 'Collins'),
    (23, 'Marketing Department Head', 40, 'Roz', 'Murphy'),
    (22, 'Marketing Department assistant', 32, 'Bob', 'Ulrich'),
    (25, 'Production staff Lead', 38, 'Henry', 'Doyle'),
    (1, 'Production staff', 42, 'Jane', 'Doe'),
    (2, 'Production staff', 40, 'Mark', 'Garcia'),
    (3, 'Production staff', 16, 'Mark' , 'Twain'),
    (4, 'Production staff', 40, 'Lisa', 'Mcronald'),
    (5, 'Production staff', 40, 'Ralph', 'George'),
    (6, 'Production staff', 40, 'Sieana', 'Wrangler'),
    (7, 'Production staff', 40, 'Elizabeth', 'Gomez'),
    (8, 'Production staff', 45, 'Tyler', 'Scott'),
    (9, 'Production staff', 24, 'Tiffany', 'Huntson'),
    (10, 'Production staff', 40, 'Rachel', 'Sun'),
    (11, 'Production staff', 16, 'Besty', 'Elias'),
    (12, 'Production staff', 40, 'Odalys', 'Agurrie'),
    (13, 'Production staff', 40, 'Nathaniel', 'Huenemeyer'),
    (14, 'Production staff', 32, 'Myrna', 'Barajas'),
    (15, 'Production staff', 28, 'Tommy', 'Gonzales'),
    (16, 'Production staff', 32, 'Andrew', 'Gonzales'),
    (17, 'Production staff', 32, 'Janet', 'Jimenez'),
    (18, 'Production staff', 32, 'Roxie', 'Clingger'),
    (19, 'Production staff', 32, 'Sarah', 'Jones'),
    (20, 'Production staff', 32, 'Tish', 'Johnson'),
    (21, 'Distribution Lead', 40, 'Maria', 'Costanza');

-- insert department records
INSERT INTO department (department_id, department_name, employee_id) VALUES
    (15672, 'Production', 25),
    (15692, 'Distribution', 21),
    (15620, 'Marketing', 23),
    (15646, 'Accounting', 24);

-- Additional INSERT statements to associate other employees with departments
INSERT INTO department (department_name, employee_id)
SELECT 'Production', employee_id FROM employee WHERE employee_position = 'Production staff';

INSERT INTO department (department_name, employee_id)
SELECT 'Marketing', employee_id FROM employee WHERE employee_position = 'Marketing Department assistant';