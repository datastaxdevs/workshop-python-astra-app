-- create employees table
CREATE TABLE sales.emp (
    empid int,
    first_name text,
    last_name text,
    PRIMARY KEY (empid)
) ;

-- insert some sample data into employees table
INSERT INTO sales.emp (empid, first_name, last_name) VALUES (1001, 'Scott', 'Tiger') ;
INSERT INTO sales.emp (empid, first_name, last_name) VALUES (1003, 'Queen', 'John') ;


SELECT * FROM sales.emp ;
