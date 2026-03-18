-- Credit Risk & Expected Loss Analytics System
-- Lending Club dataset 2007-2018
-- All queries run against the loans table in credit_risk.db


-- 1. Portfolio summary
SELECT
    COUNT(*) as total_loans,
    ROUND(SUM(loan_amnt), 2) as total_loan_amount,
    ROUND(AVG(default_flag) * 100, 2) as overall_default_rate_pct,
    ROUND(SUM(EAD), 2) as total_EAD,
    ROUND(SUM(ECL), 2) as total_ECL,
    ROUND(SUM(ECL) / SUM(EAD) * 100, 2) as portfolio_ECL_pct,
    ROUND(AVG(int_rate), 2) as avg_interest_rate,
    ROUND(AVG(loan_amnt), 2) as avg_loan_amount
FROM loans;


-- 2. ECL breakdown by loan grade
SELECT
    grade,
    COUNT(*) as total_loans,
    SUM(default_flag) as total_defaults,
    ROUND(AVG(default_flag) * 100, 2) as PD_pct,
    ROUND((1 - AVG(recoveries / funded_amnt)) * 100, 2) as LGD_pct,
    ROUND(SUM(EAD), 2) as total_EAD,
    ROUND(SUM(ECL), 2) as total_ECL,
    ROUND(SUM(ECL) / SUM(EAD) * 100, 2) as ECL_pct
FROM loans
WHERE funded_amnt > 0
GROUP BY grade
ORDER BY grade;


-- 3. Vintage analysis — default rate and ECL by issue year
SELECT
    issue_year,
    COUNT(*) as total_loans,
    SUM(default_flag) as total_defaults,
    ROUND(AVG(default_flag) * 100, 2) as default_rate_pct,
    ROUND(SUM(EAD), 2) as total_EAD,
    ROUND(SUM(ECL), 2) as total_ECL,
    ROUND(SUM(ECL) / SUM(EAD) * 100, 2) as ECL_pct
FROM loans
GROUP BY issue_year
ORDER BY issue_year;


-- 4. Top 10 riskiest sub-grades by default rate
SELECT
    sub_grade,
    COUNT(*) as total_loans,
    SUM(default_flag) as total_defaults,
    ROUND(AVG(default_flag) * 100, 2) as PD_pct,
    ROUND(SUM(ECL), 2) as total_ECL,
    ROUND(SUM(ECL) / SUM(EAD) * 100, 2) as ECL_pct
FROM loans
WHERE funded_amnt > 0
GROUP BY sub_grade
ORDER BY PD_pct DESC
LIMIT 10;


-- 5. Default rate by loan term (36 vs 60 months)
SELECT
    term,
    COUNT(*) as total_loans,
    SUM(default_flag) as total_defaults,
    ROUND(AVG(default_flag) * 100, 2) as default_rate_pct,
    ROUND(AVG(int_rate), 2) as avg_interest_rate,
    ROUND(SUM(ECL), 2) as total_ECL,
    ROUND(SUM(ECL) / SUM(EAD) * 100, 2) as ECL_pct
FROM loans
GROUP BY term
ORDER BY term;


-- 6. Risk segmentation by DTI (debt-to-income ratio)
SELECT
    CASE
        WHEN dti < 10 THEN 'Low DTI (< 10)'
        WHEN dti BETWEEN 10 AND 20 THEN 'Medium DTI (10-20)'
        WHEN dti BETWEEN 20 AND 30 THEN 'High DTI (20-30)'
        ELSE 'Very High DTI (> 30)'
    END as dti_segment,
    COUNT(*) as total_loans,
    ROUND(AVG(default_flag) * 100, 2) as default_rate_pct,
    ROUND(AVG(loan_amnt), 2) as avg_loan_amount,
    ROUND(SUM(ECL), 2) as total_ECL,
    ROUND(SUM(ECL) / SUM(EAD) * 100, 2) as ECL_pct
FROM loans
GROUP BY dti_segment
ORDER BY default_rate_pct DESC;


-- 7. Default rate by interest rate bucket
SELECT
    CASE
        WHEN int_rate < 8 THEN 'Low (< 8%)'
        WHEN int_rate BETWEEN 8 AND 12 THEN 'Medium (8-12%)'
        WHEN int_rate BETWEEN 12 AND 18 THEN 'High (12-18%)'
        WHEN int_rate BETWEEN 18 AND 24 THEN 'Very High (18-24%)'
        ELSE 'Extreme (> 24%)'
    END as rate_segment,
    COUNT(*) as total_loans,
    ROUND(AVG(default_flag) * 100, 2) as default_rate_pct,
    ROUND(AVG(loan_amnt), 2) as avg_loan_amount,
    ROUND(SUM(ECL), 2) as total_ECL,
    ROUND(SUM(ECL) / SUM(EAD) * 100, 2) as ECL_pct
FROM loans
GROUP BY rate_segment
ORDER BY default_rate_pct DESC;