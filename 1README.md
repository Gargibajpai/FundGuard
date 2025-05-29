# FundGuard - Government Tender Analysis Tool
FundGuard is a web application that helps analyze government tender data to identify potential risks and anomalies in tender allocations.
# Problem Statement

Government tenders often involve large sums of public money, and inefficiencies or fraudulent practices can go unnoticed. There’s a need for an accessible tool that flags suspicious tenders based on predefined criteria, helping authorities and watchdogs identify potential red flags in public procurement.

## Features

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
Frontend: HTML5, Bootstrap 5, Chart.js

Backend: Python Flask

Data Processing: Pandas

Deployment Ready: Easily deployable on platforms like Heroku or Render

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/FundGuard.git
cd FundGuard
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a CSV file with the following columns:
   - Tender ID
   - Department
   - Vendor
   - Estimated Cost
   - Final Cost
   - Start Date
   - End Date
   - State

4. View the analysis results in the dashboard and download flagged tenders if needed.

## CSV Format

Your CSV file should follow this format:
```csv
Tender ID,Department,Vendor,Estimated Cost,Final Cost,Start Date,End Date,State
T001,Public Works,Vendor A,100000,120000,2024-01-01,2024-06-30,California
```

## Contributing

Feel free to submit issues and enhancement requests! 