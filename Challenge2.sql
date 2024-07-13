----------------------------------------------------------------------------
---#Challenge 2:
--Imagine you are designing a database schema for a system that manages workers' compensation claims and uses machine learning models for prediction and analysis.
--Objective 2.1:
--Design the database schema with appropriate tables to store the following information:
--1.	Workers' details
--2.	Claims data
--3.	Machine learning model predictions (Use Model from Challenge 1)
--Provide the SQL schema for the database, including table definitions, primary keys, foreign keys, and any necessary relationships or constraints.

--Schema Workers' details
CREATE TABLE Workers (
    WorkerId INT PRIMARY KEY,
    WorkerName VARCHAR(100) NOT NULL,
    DateOfBirth DATE,
    Occupation VARCHAR(100),
    CONSTRAINT chk_DateOfBirth CHECK (DateOfBirth <= CURRENT_DATE)--incase incorrect DOB has been added
);


--2.	Claims data
CREATE TABLE Claims (
    CaseNumber INT PRIMARY KEY,
    WorkerId INT,
    ClaimDate DATE,
    ClaimCost DECIMAL(12, 2),
    Litigation VARCHAR(3) CHECK (Litigation IN ('YES', 'NO')),
    LossType VARCHAR(50),
    Carrier VARCHAR(50),
    Sector/Industry VARCHAR(100),
    HighCost BIT,
    FOREIGN KEY (WorkerId) REFERENCES Workers(WorkerId)
);

--3.	Machine learning model predictions (Use Model from Challenge 1)
CREATE TABLE ModelPredictions (
    PredictionId INT PRIMARY KEY,
    CaseNumber INT,
    Prediction FLOAT,
    ModelName VARCHAR(50),
    PredictionDate DATE,
    FOREIGN KEY (CaseNumber) REFERENCES Claims(CaseNumber)
);

--Objective 2.2:
--Provide SQL queries to:
--1.	Retrieve workers' details along with their total claimed costs.
SELECT 
    w.WorkerId,
    w.WorkerName,
    SUM(c.ClaimCost) AS TotalCost
FROM Workers w
LEFT JOIN Claims c ON w.WorkerId = c.WorkerId
GROUP BY w.WorkerId, w.WorkerName;


--2.	Calculate average claim costs based on industry types.
SELECT 
    Sector/Industry,
    AVG(ClaimCost) AS AverageClaimCost
FROM Claims
GROUP BY Sector/Industry;
