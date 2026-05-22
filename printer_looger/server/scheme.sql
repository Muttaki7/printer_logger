CREATE TABLE printers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    printer_name VARCHAR(100) NOT NULL,
    department ENUM('Knitting', 'Legal', 'IT', 'Mechanic', 'Technician') NOT NULL,
    level VARCHAR(50),
    model_number VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE print_jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    print_id VARCHAR(50) UNIQUE NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    page_amount INT NOT NULL CHECK (page_amount > 0),
    copies INT DEFAULT 1,
    department ENUM('Knitting', 'Legal', 'IT', 'Mechanic', 'Technician') NOT NULL,
    assigned_printer_id INT,
    printer_model_number VARCHAR(100),
    status ENUM('pending', 'printed', 'deleted') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    print_start_time TIMESTAMP NULL,
    job_type VARCHAR(50) DEFAULT 'Hold Print',
    FOREIGN KEY (assigned_printer_id) REFERENCES printers(id) ON DELETE SET NULL
);

-- ------------------------------
-- Department-based seed data
-- ------------------------------
-- Note: This is optional MySQL seed data for documentation/testing.
-- The running backend uses MongoDB.

-- Knitting printers
INSERT INTO printers (printer_name, department, level, model_number, ip_address, is_active)
VALUES
  ('Knitting_Printer_1', 'Knitting', 'Level 1', 'RICOH MP 4100', '192.168.1.201', TRUE),
  ('Knitting_Printer_2', 'Knitting', 'Level 2', 'RICOH MP 4101', '192.168.1.202', TRUE),
  ('Knitting_Printer_3', 'Knitting', 'Level 3', 'RICOH MP 4102', '192.168.1.203', TRUE),
  ('Knitting_Printer_4', 'Knitting', 'Level 1', 'RICOH MP 4103', '192.168.1.204', TRUE),
  ('Knitting_Printer_5', 'Knitting', 'Level 2', 'RICOH MP 4104', '192.168.1.205', TRUE),
  ('Knitting_Printer_6', 'Knitting', 'Level 3', 'RICOH MP 4105', '192.168.1.206', TRUE),
  ('Knitting_Printer_7', 'Knitting', 'Level 1', 'RICOH MP 4106', '192.168.1.207', TRUE),
  ('Knitting_Printer_8', 'Knitting', 'Level 2', 'RICOH MP 4107', '192.168.1.208', TRUE),
  ('Knitting_Printer_9', 'Knitting', 'Level 3', 'RICOH MP 4108', '192.168.1.209', TRUE),
  ('Knitting_Printer_10', 'Knitting', 'Level 1', 'RICOH MP 4109', '192.168.1.210', TRUE);


-- Legal printers
INSERT INTO printers (printer_name, department, level, model_number, ip_address, is_active)
VALUES
  ('Legal_Printer_1', 'Legal', 'Level 1', 'HP LaserJet M 4200', '192.168.1.221', TRUE),
  ('Legal_Printer_2', 'Legal', 'Level 2', 'HP LaserJet M 4201', '192.168.1.222', TRUE),
  ('Legal_Printer_3', 'Legal', 'Level 3', 'HP LaserJet M 4202', '192.168.1.223', TRUE),
  ('Legal_Printer_4', 'Legal', 'Level 1', 'HP LaserJet M 4203', '192.168.1.224', TRUE),
  ('Legal_Printer_5', 'Legal', 'Level 2', 'HP LaserJet M 4204', '192.168.1.225', TRUE);

-- IT printers
INSERT INTO printers (printer_name, department, level, model_number, ip_address, is_active)
VALUES
  ('IT_Printer_1', 'IT', 'Level 1', 'RICOH IM C 4300', '192.168.1.241', TRUE),
  ('IT_Printer_2', 'IT', 'Level 2', 'RICOH IM C 4301', '192.168.1.242', TRUE),
  ('IT_Printer_3', 'IT', 'Level 3', 'RICOH IM C 4302', '192.168.1.243', TRUE),
  ('IT_Printer_4', 'IT', 'Level 1', 'RICOH IM C 4303', '192.168.1.244', TRUE),
  ('IT_Printer_5', 'IT', 'Level 2', 'RICOH IM C 4304', '192.168.1.245', TRUE);

-- Mechanic printers
INSERT INTO printers (printer_name, department, level, model_number, ip_address, is_active)
VALUES
  ('Mechanic_Printer_1', 'Mechanic', 'Level 1', 'Brother HL-L 4400', '192.168.1.261', TRUE),
  ('Mechanic_Printer_2', 'Mechanic', 'Level 2', 'Brother HL-L 4401', '192.168.1.262', TRUE),
  ('Mechanic_Printer_3', 'Mechanic', 'Level 3', 'Brother HL-L 4402', '192.168.1.263', TRUE),
  ('Mechanic_Printer_4', 'Mechanic', 'Level 1', 'Brother HL-L 4403', '192.168.1.264', TRUE),
  ('Mechanic_Printer_5', 'Mechanic', 'Level 2', 'Brother HL-L 4404', '192.168.1.265', TRUE);

-- Technician printers
INSERT INTO printers (printer_name, department, level, model_number, ip_address, is_active)
VALUES
  ('Technician_Printer_1', 'Technician', 'Level 1', 'Xerox VersaLink C 4500', '192.168.1.281', TRUE),
  ('Technician_Printer_2', 'Technician', 'Level 2', 'Xerox VersaLink C 4501', '192.168.1.282', TRUE),
  ('Technician_Printer_3', 'Technician', 'Level 3', 'Xerox VersaLink C 4502', '192.168.1.283', TRUE),
  ('Technician_Printer_4', 'Technician', 'Level 1', 'Xerox VersaLink C 4503', '192.168.1.284', TRUE),
  ('Technician_Printer_5', 'Technician', 'Level 2', 'Xerox VersaLink C 4504', '192.168.1.285', TRUE);

