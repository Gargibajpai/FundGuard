# FundGuard – Government Tender Risk Analyzer
A data-driven platform that detects corruption patterns in government tender allocations using CSV data and visual analytics.

# PROBLEM STATEMENT
Government tenders often involve large sums of public money, and inefficiencies or fraudulent practices can go unnoticed. There’s a need for an accessible tool that flags suspicious tenders based on predefined criteria, helping authorities and watchdogs identify potential red flags in public procurement.

#  APPROACH & SOLUTION
FundGuard is a Flask-based web application that allows users to upload CSV files containing government tender data. It analyzes the data using Pandas and flags potentially suspicious entries based on:
-Excessive final cost (Final Cost > 1.5 × Estimated Cost)
-Frequent vendor wins (same vendor wins more than 3 tenders)
-The app offers an interactive dashboard and risk report to support transparency and audit-readiness.

#  FEATURES 
  - Upload and analyze CSV files containing tender data
- Automatic risk flagging for:
  - Over-budget tenders (Final Cost > 1.5 × Estimated Cost)
  - Repeated vendor allocations (same vendor winning > 3 tenders)
- Interactive dashboard with:
  - Total tenders count
  - Flagged tenders count
  - Risk distribution pie chart
- Downloadable report of flagged tenders
- Responsive data table with all tender details
  
 # Tech Stack
   Frontend: HTML5, Bootstrap 5, Chart.js,
   Backend: Python Flask,
   Data Processing: Pandas,
   Deployment Ready: Easily deployable on platforms like Heroku or Render.

