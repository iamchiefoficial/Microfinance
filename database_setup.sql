-- MySQL Database Setup for Microfinance Platform
-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS microfinance_db;
USE microfinance_db;

-- Create users table
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    national_id VARCHAR(50) UNIQUE NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    monthly_income DECIMAL(12,2) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'client',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create loans table
CREATE TABLE IF NOT EXISTS loan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    purpose VARCHAR(200) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    current_stage VARCHAR(50) NOT NULL DEFAULT 'loan_officer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES user(id)
);

-- Create loan_approvals table
CREATE TABLE IF NOT EXISTS loan_approval (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    approver_id INT NOT NULL,
    stage VARCHAR(50) NOT NULL,
    decision VARCHAR(20) NOT NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (loan_id) REFERENCES loan(id),
    FOREIGN KEY (approver_id) REFERENCES user(id)
);

-- Production system - no demo accounts included
-- Staff accounts should be created through admin interface or direct database insertion
