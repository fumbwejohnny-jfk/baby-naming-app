# 🚀 Name Intelligence Platform

## 🧠 1. Overview
This application assists prospective parents in selecting meaningful and well-informed names for their future children.

The system will provide:
* Historical trends of baby names 
* Gender-based usage analysis 
* Meaning and origin of names 

👉 The goal is to transform simple name lookup into a data-driven decision platform.

---

## 🎯 2. Objectives
The application:
* Enable end-users to explore, analyze, and visualize baby name data 
* Deliver insightful analytics (bar charts & pie chart) to support decision-making 

---

## 👥 3. User Roles & Responsibilities

### 👤 3.1 End-User (Parent)
The end-user interacts with the system to explore and analyze baby names.

#### Capabilities:

#### 🔍 Browse Names
* View all baby names in a searchable and sortable table 
* Filter by: 
  * Gender 
  * Year 
  * Popularity 

---

#### 📊 Trend Analysis
* Input a baby name to: 
  * View usage trends over time 
  * Analyze popularity per gender 

**Visualizations:**
* 📈 Line Chart → trend over years 
* 🥧 Pie Chart → gender distribution 

---

#### 📖 Meaning Lookup
* Search for a name 
* Display: 
  * Meaning 

---

## 📊 4. Example Use Case

### Scenario:
A parent wants to evaluate the name “Liam”

### Steps:
1. User logs in 
2. Searches for “Liam” 
3. System retrieves: 
   * Meaning 
   * Usage over years 
4. Displays: 
   * Line chart (trend) 
   * Pie chart (gender distribution) 

👉 User gains insight into popularity and meaning

---

## 🛠️ 5. Technology Stack
* **Language:** Python 
* **UI Options:** 
  * Tkinter / PyQt (desktop) 
  * Numpy, matplotlib

## 🛠️ 6. Project Structure
│
├── babay-app/
│   ├── library/                    # utility functions
│       └── stat.py
│       └── baby.py
│       └── baby_library.py
│       └── baby_stats_library.py
│   ├── model/                      # baby model
│       └── babyName.py                      
│   ├── names/                      # folder containing .txt and .csv files
│   ├── pages/                      # app's pages
│       └── AdminPage.py
│       └── LoginPage.py
│       └── MainPage.py
│       └── UserPage.py
│   └── requirements.txt
│   └── generate.sh                 # script to generate JSON files
│   └── run.sh                      # script to run the app
│   └── readme.sh
│

## 🛠️ 7. How to run the Baby-app
1. Clone the repository
   git clone <repository-url>
   cd repository
2. Create and activate virtual environment
   python3 -m venv venv             (create python environment)
   source venv/bin/activate         (activate python environment in linux/bash/ubuntu)  
   or venv\Scripts\activate         (activate python environement in windows) 
3. Install dependencies
   pip install -r requirements.txt  (install python packages)
4. ./generate.sh                    (script to generate JSON files)
5. ./run.sh                         (script to run baby-app)

