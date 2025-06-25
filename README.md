# FundGuard – Government Tender Risk Analyzer
A visually appealing web app to detect corruption in government tenders.
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
   * Frontend: HTML5, Bootstrap 5, Chart.js
   * Backend: Python Flask
   * Data Processing: Pandas
   * Deployment Ready: Easily deployable on platforms like Heroku or Render
     
# Installation & Usage
🧰 Setup Instructions
1. Clone the repository:
 
``` git clone https://github.com/Gargibajpai/FundGuard.git```

```cd FundGuard```

3. (Optional) Create and activate a virtual environment:
# Windows
```python -m venv venv```

```venv\Scripts\activate```

# macOS/Linux
```python3 -m venv venv```

```source venv/bin/activate```

3. Install dependencies:
   
  ```pip install -r requirements.txt```

5. Run the app:
   
  ```python app.py```

7. Visit: ```http://127.0.0.1:5000```
   

9. 🔐 Login Details
Use these credentials to log in:

Username: admin

Password: admin123



## 📸 Demo Screenshot

Here’s a preview of the FundGuard dashboard in action:
![image](https://github.com/user-attachments/assets/e5a363d7-baf9-4098-b01a-b7bb033cd3af)

![image](https://github.com/user-attachments/assets/01988e6d-58c2-4723-aec5-38e7a37610b0)

![image](https://github.com/user-attachments/assets/b5c53211-7116-45c9-824c-e3eac1710a39)

![image](https://github.com/user-attachments/assets/192c27f9-c6df-482f-b363-b71c4375d022)

