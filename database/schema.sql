CREATE DATABASE manufacturing_analytics;
USE manufacturing_analytics;

CREATE TABLE Factories (
    factory_id        INT AUTO_INCREMENT PRIMARY KEY,
    factory_name      VARCHAR(100) NOT NULL,
    location          VARCHAR(100) NOT NULL,
    manager_name      VARCHAR(100) NOT NULL,
    established_date  DATE NOT NULL
);


CREATE TABLE Shifts (
    shift_id    INT AUTO_INCREMENT PRIMARY KEY,
    shift_name  VARCHAR(50) NOT NULL,
    start_time  TIME NOT NULL,
    end_time    TIME NOT NULL,
    CONSTRAINT chk_shift_times CHECK (start_time <> end_time)
);

CREATE TABLE Employees (
    employee_id      INT AUTO_INCREMENT PRIMARY KEY,
    employee_name    VARCHAR(100) NOT NULL,
    designation      VARCHAR(50) NOT NULL,
    experience_years INT NOT NULL,
    salary           DECIMAL(10,2) NOT NULL,
    hire_date        DATE NOT NULL,
    factory_id       INT NOT NULL,
    shift_id         INT NOT NULL,
    CONSTRAINT fk_employee_factory FOREIGN KEY (factory_id) REFERENCES Factories(factory_id),
    CONSTRAINT fk_employee_shift   FOREIGN KEY (shift_id)   REFERENCES Shifts(shift_id),
    CONSTRAINT chk_employee_experience CHECK (experience_years >= 0),
    CONSTRAINT chk_employee_salary     CHECK (salary > 0)
);

CREATE TABLE Machines (
    machine_id        INT AUTO_INCREMENT PRIMARY KEY,
    machine_name      VARCHAR(100) NOT NULL,
    machine_type      VARCHAR(50) NOT NULL,
    installation_date DATE NOT NULL,
    status            ENUM('Running', 'Idle', 'Under Maintenance', 'Retired') NOT NULL DEFAULT 'Idle',
    last_service_date DATE,
    factory_id        INT NOT NULL,
    CONSTRAINT fk_machine_factory FOREIGN KEY (factory_id) REFERENCES Factories(factory_id),
    CONSTRAINT chk_machine_service_date CHECK (last_service_date IS NULL OR last_service_date >= installation_date)
);

CREATE TABLE Products (
    product_id     INT AUTO_INCREMENT PRIMARY KEY,
    product_name   VARCHAR(100) NOT NULL,
    category       VARCHAR(50) NOT NULL,
    unit_cost      DECIMAL(10,2) NOT NULL,
    selling_price  DECIMAL(10,2) NOT NULL,
    CONSTRAINT chk_product_unit_cost     CHECK (unit_cost > 0),
    CONSTRAINT chk_product_selling_price CHECK (selling_price > 0),
    CONSTRAINT chk_product_margin        CHECK (selling_price >= unit_cost)
);

CREATE TABLE Production_Batches (
    production_id     INT AUTO_INCREMENT PRIMARY KEY,
    production_date   DATE NOT NULL,
    machine_id        INT NOT NULL,
    employee_id       INT NOT NULL,
    product_id        INT NOT NULL,
    shift_id          INT NOT NULL,
    units_produced    INT NOT NULL,
    defective_units   INT NOT NULL DEFAULT 0,
    production_hours  DECIMAL(5,2) NOT NULL,
    CONSTRAINT fk_prodbatch_machine  FOREIGN KEY (machine_id)  REFERENCES Machines(machine_id),
    CONSTRAINT fk_prodbatch_employee FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    CONSTRAINT fk_prodbatch_product  FOREIGN KEY (product_id)  REFERENCES Products(product_id),
    CONSTRAINT fk_prodbatch_shift    FOREIGN KEY (shift_id)    REFERENCES Shifts(shift_id),
    CONSTRAINT chk_prodbatch_units_produced  CHECK (units_produced > 0),
    CONSTRAINT chk_prodbatch_defective_units CHECK (defective_units >= 0),
    CONSTRAINT chk_prodbatch_defects_le_units CHECK (defective_units <= units_produced),
    CONSTRAINT chk_prodbatch_hours CHECK (production_hours > 0 AND production_hours <= 24)
);

CREATE TABLE Maintenance (
    maintenance_id     INT AUTO_INCREMENT PRIMARY KEY,
    machine_id         INT NOT NULL,
    maintenance_date   DATE NOT NULL,
    maintenance_type   ENUM('Preventive', 'Corrective', 'Emergency') NOT NULL,
    downtime_hours     DECIMAL(5,2) NOT NULL,
    maintenance_cost   DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_maintenance_machine FOREIGN KEY (machine_id) REFERENCES Machines(machine_id),
    CONSTRAINT chk_maintenance_downtime CHECK (downtime_hours >= 0 AND downtime_hours <= 24),
    CONSTRAINT chk_maintenance_cost     CHECK (maintenance_cost >= 0)
);
 

CREATE TABLE Defects (
    defect_id          INT AUTO_INCREMENT PRIMARY KEY,
    production_id      INT NOT NULL,
    defect_type        VARCHAR(50) NOT NULL,
    severity            ENUM('Low', 'Medium', 'High') NOT NULL,
    defect_description  TEXT,
    CONSTRAINT fk_defect_production FOREIGN KEY (production_id) REFERENCES Production_Batches(production_id)
);
 

CREATE TABLE Quality_Inspection (
    inspection_id      INT AUTO_INCREMENT PRIMARY KEY,
    production_id       INT NOT NULL,
    inspector_id         INT NOT NULL,
    inspection_date      DATE NOT NULL,
    inspection_result    ENUM('Pass', 'Fail') NOT NULL,
    remarks               TEXT,
    CONSTRAINT fk_inspection_production FOREIGN KEY (production_id) REFERENCES Production_Batches(production_id),
    CONSTRAINT fk_inspection_inspector  FOREIGN KEY (inspector_id)  REFERENCES Employees(employee_id)
);

CREATE INDEX idx_prodbatch_date     ON Production_Batches(production_date);
CREATE INDEX idx_maintenance_date   ON Maintenance(maintenance_date);
CREATE INDEX idx_inspection_date    ON Quality_Inspection(inspection_date);
CREATE INDEX idx_inspection_result  ON Quality_Inspection(inspection_result);







