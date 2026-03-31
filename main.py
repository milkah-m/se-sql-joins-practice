import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

#1. Select the names (first and last) of all employees in Boston.

q = """
SELECT firstName, lastName
FROM employees
JOIN offices
USING (officeCode)
WHERE offices.city = "Boston"
"""
print(pd.read_sql(q, conn))

#2. Are there any offices that have zero employees?

q = """
SELECT *
FROM offices
LEFT JOIN employees
USING (officeCode)
"""
df = pd.read_sql(q, conn)

print("Length of data frame:", len(df))
print("Number of null records:", len(df[df.employeeNumber.isnull()]))
print(df[df.employeeNumber.isnull()])

#3. How many customers are there per office?

q = """
SELECT 
    o.officeCode,
    COUNT(c.customerNumber) AS num_customers
FROM offices o
LEFT JOIN employees e 
    USING(officeCode)
LEFT JOIN customers c 
    ON c.salesRepEmployeeNumber = e.employeeNumber
GROUP BY o.officeCode
"""
df = pd.read_sql(q, conn)

print(df)

#4. Display the names of every individual product that each employee has sold as a dataframe.
q = """
SELECT 
    e.employeeNumber,
    e.lastName,
    e.firstName,
    p.productName
FROM employees e
JOIN customers c 
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o 
    ON c.customerNumber = o.customerNumber
JOIN orderdetails od 
    ON o.orderNumber = od.orderNumber
JOIN products p 
    ON od.productCode = p.productCode
ORDER BY e.employeeNumber, p.productName;
"""

df = pd.read_sql(q, conn)

print(df)

#5. Display the number of products each employee has sold
# - Alphabetize the results by employee last name.
# - Use the quantityOrdered column from orderDetails.
# - Think about how to group the data when some employees might have the same first or last name.

q = """SELECT 
    e.employeeNumber,
    e.lastName,
    e.firstName,
    SUM(od.quantityOrdered) AS total_products_sold
FROM employees e
JOIN customers c 
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o 
    ON c.customerNumber = o.customerNumber
JOIN orderdetails od 
    ON o.orderNumber = od.orderNumber
GROUP BY e.employeeNumber, e.lastName, e.firstName
ORDER BY e.lastName;"""

print(pd.read_sql(q, conn))

#6.  Display the names of employees who have sold more than 200 different products.

q = """SELECT 
    e.employeeNumber,
    e.lastName,
    e.firstName,
    COUNT(DISTINCT od.productCode) AS distinct_products_sold
FROM employees e
JOIN customers c 
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o 
    ON c.customerNumber = o.customerNumber
JOIN orderdetails od 
    ON o.orderNumber = od.orderNumber
GROUP BY e.employeeNumber, e.lastName, e.firstName
HAVING COUNT(DISTINCT od.productCode) > 200
ORDER BY e.lastName;
"""
print(pd.read_sql(q, conn))

conn.close()