-- Add approved_by column to loans table
ALTER TABLE loans ADD COLUMN approved_by VARCHAR(100) DEFAULT NULL;

-- Update existing loans to set approved_by based on current stage
UPDATE loans 
SET approved_by = CASE 
    WHEN current_stage = 'loan_officer' THEN 'Loan Officer'
    WHEN current_stage = 'loan_manager' THEN 'Loan Manager'
    WHEN current_stage = 'general_director' THEN 'General Director'
    WHEN current_stage = 'managing_director' THEN 'Managing Director'
    ELSE current_stage
END
WHERE approved_by IS NULL;
