## ECE568 Spring 2018 Homework1 01/31/2018
**Name**: Zhongze Tang  **NetID**: zt67  
**E-mail**: zhongze.tang@rutgers.edu

## Question 1
### (1)
![ER](https://s1.ax1x.com/2018/02/03/9VObnA.png)
### (2)
```sql
CREATE TABLE certifications
(
  employee           CHAR(20) DEFAULT '' NOT NULL,
  certification_name CHAR(20) DEFAULT '' NOT NULL,
  PRIMARY KEY (employee, certification_name)
)
  ENGINE = MyISAM;

CREATE TABLE customer
(
  SSN  CHAR(11) NOT NULL
    PRIMARY KEY,
  name CHAR(20) NULL,
  age  INT      NULL,
  CONSTRAINT customer_SSN_uindex
  UNIQUE (SSN)
)
  ENGINE = MyISAM;

CREATE TABLE employee
(
  SSN            CHAR(11) NOT NULL
    PRIMARY KEY,
  name           CHAR(20) NULL,
  specialization CHAR(20) NULL,
  CONSTRAINT employee_SSN_uindex
  UNIQUE (SSN)
)
  ENGINE = MyISAM;

CREATE TABLE go_to
(
  customer CHAR(11) NULL,
  gym      CHAR(40) NULL
)
  ENGINE = MyISAM;

CREATE INDEX customer_SSN
  ON go_to (customer);

CREATE INDEX gym_name
  ON go_to (gym);

CREATE TABLE guest
(
  name     CHAR(20) NULL,
  age      INT      NULL,
  customer CHAR(11) NULL
)
  ENGINE = MyISAM;

CREATE INDEX customer_SSN
  ON guest (customer);

CREATE TABLE gym
(
  name        CHAR(20) NOT NULL
    PRIMARY KEY,
  street_no   INT      NULL,
  street_name CHAR(40) NULL,
  zip_code    INT      NULL,
  manager     CHAR(11) NOT NULL,
  CONSTRAINT gym_name_uindex
  UNIQUE (name)
)
  ENGINE = MyISAM;

CREATE INDEX manager_SSN
  ON gym (manager);

CREATE TABLE phone_no
(
  phone_no INT      NOT NULL
    PRIMARY KEY,
  gym      CHAR(20) NULL,
  CONSTRAINT phone_no_phone_no_uindex
  UNIQUE (phone_no)
)
  ENGINE = MyISAM;

CREATE INDEX gym_name
  ON phone_no (gym);

CREATE TABLE work_at
(
  gym       CHAR(20) NOT NULL,
  employee  CHAR(11) NOT NULL,
  percetage INT      NOT NULL,
  PRIMARY KEY (gym, employee, percetage)
)
  ENGINE = MyISAM;

CREATE INDEX employee_SSN
  ON work_at (employee);


```
## Question 2
### (1)
```sql
SELECT S.sname
FROM Suppliers S
WHERE NOT EXISTS((SELECT P.pid
                  FROM Parts P)
                EXCEPT
                (SELECT C.pid
                 FROM Catalog C
                 WHERE C.sid = S.sid))
```
### (2)
```sql
SELECT C.sid
FROM Catalog C
WHERE C.cost > (SELECT AVG(C1.cost)
               FROM Catalog C1
               WHERE C1.pid = C.pid)
```
### (3)
```sql
SELECT P.pid, S.sname
FROM Parts P, Suppliers S, Catalog C
WHERE P.pid = C.pid AND C.sid = S.sid
    AND C.cost >= ALL(SELECT C1.cost
                      FROM Catalog C1
                      WHERE C1.pid = C.pid)
```
### (4)
```sql
SELECT C.sid
FROM Catalog C
WHERE NOT EXISTS(SELECT P.color
                 FROM Parts P
                 WHERE P.color <> "red"
                    AND P.pid = C.pid)
```
### (5)
```sql
SELECT C.sid
FROM Catalog C
WHERE EXISTS(SELECT P.color
             FROM Parts P
             WHERE (P.color = "green" OR P.color = "red")
                AND P.pid = C.pid)
```
### (6)
```sql
SELECT S.sname, MAX(C.cost)
FROM Suppliers S, Catalog C, Parts P
WHERE S.sid = C.sid, C.pid = P.pid
GROUP BY S.sid
HAVING ANY(P.color = "red") AND ANY(P.color = "green")
```

## Question 3
### 1)
```sql
SELECT M.MovieName
FROM Movies M, MovieSupplier MS, Suppliers S
WHERE (S.SupplierName = "Ben's Video" OR S.SupplierName = "Video Clubhouse")
    AND M.MovieID = MS.MovieID AND S.SupplierID = MS.SupplierID
```
### 2)
```sql
SELECT M.MovieName
FROM Movies M, Rentals R, Inventory I
WHERE M.MovieID = I.MovieID AND I.TapeID = R.TapeID
    AND R.Duration >= ALL(SELECT Duration FROM Rentals)
```
### 3)
```sql
SELECT S.SupplierName
FROM Supplier S
WHERE S.SupplierID NOT IN
    (SELECT MS.SupplierID
     FROM MovieSupplier MS, Inventory I
     WHERE NOT EXISTS
        (SELECT *
         FROM MovieSupplier MS2, Inventory I2
         WHERE MS2.MovieID = I2.MovieID
            AND I2.MovieID = I.MovieID
            AND MS2.SupplierID = MS.SupplierID))
```
### 4)
```sql
SELECT S.SupplierName, COUNT(DISTINC MovieID)
FROM Suppliers S, MovieSupplier MS
WHERE S.SupplierID = MS.SupplierID
GROUP BY S.SupplierName
```
### 5)
```sql
SELECT M.MovieName
FROM Movies M, Orders O
WHERE M.MovieID = O.MovieID
GROUP BY M.MovieName
HAVING SUM(O.copies) > 4
```
### 6)
```sql
SELECT C.LastName, C.FirstName
FROM Customers C, Rentals R, Inventory I, Movies M
WHERE C.CustID = R.CustomerID AND R.TapeID = I.TapeID
    AND I.MovieID = M.MovieID AND M.MovieName = "Kung Fu Panda"
UNION
SELECT C.LastName, C.FirstName
FROM Customers C, Rentals R, Inventory I, MovieSupplier MS, Suppliers S
WHERE C.CustID = R.CustomerID AND R.TapeID = I.TapeID
    AND I.MovieID = MS.MovieID AND MS.SupplierID = S.SupplierID
    AND S.SupplierName = "Palm Video"
```
### 7)
```sql
SELECT M.MovieName
FROM Movies M, Inventory I1, Inventory I2
WHERE I1.TapeID <> I2.TapeID AND I1.MovieID = I2.MovieID
    AND I1.MovieID = M.MovieID
```
### 8)
```sql
SELECT C.LastName, C.FirstName
FROM Customers C, Rentals R
WHERE C.CustID = R.CustomerID AND R.Duration>=5
```
### 9)
```sql
SELECT S.SupplierName
FROM Suppliers S, MovieSupplier MS, Movies M
WHERE S.SupplierID = MS.SupplierID AND M.MovieName = "Cinderella 2015"
    AND M.MovieID = MS.MovieID
    AND MS.Price <= ALL(SELECT Price
                        FROM MovieSupplier MS, Movies M
                        WHERE MS.MovieID = M.MovieID
                            AND M.MovieName = "Cinderella 2015")
```
### 10)
```sql
SELECT MovieName
FROM Movies
WHERE Movies.MovieID NOT IN
    (SELECT MovieID
    FROM Inventory)
```
## Question 4
After doing some research on triggers, I find that a trigger will not call itself recursively by default. That is, an update trigger does not call itself in response to a second update to the same table within the trigger.

And I suppose the data type of price is **float**.

If the trigger calls itself recursively, the results will be 3, 0.75, 0.75, respectively.
### a)
The price of pruchaseID #111 will be set to 3.
It will execute statements in the order of:
```sql
UPDATE Purchase
SET price = 1.5
WHERE purchaseID = 111

/* the original SQL statement */
UPDATE Purchase
SET price = 3
WHERE purchaseID = 111
```
### b)
The price of pruchaseID #111 will be set to 1.5.
It will execute statements in the order of:
```sql
/* the original SQL statement */
UPDATE Purchase
SET price = 3
WHERE purchaseID = 111

UPDATE Purchase
SET price = 1.5
WHERE purchaseID = 111
```
### c)
The price of pruchaseID #111 will be set to 1.5.
It will execute statements in the order of:
```sql
UPDATE Purchase
SET price = 1.5
WHERE purchaseID = 111
```
