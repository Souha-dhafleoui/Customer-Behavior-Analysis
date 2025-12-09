# Customer Behavior Analysis - Business Intelligence Project


##  Project Overview
A comprehensive Business Intelligence project analyzing customer purchasing behavior using ETL workflows, SQL analysis, and Power BI visualization. The project integrates multi-source customer data to uncover insights for segmentation and strategic business recommendations.

##  Key Objectives
- Build an ETL pipeline to integrate data from multiple sources
- Create a star schema data warehouse
- Perform in-depth customer behavior analysis using SQL
- Generate actionable insights through Power BI dashboards
- Provide data-driven recommendations for marketing and sales strategies
  
---

##  Project Architecture

### Data Pipeline
Raw Data Sources → ETL Process → Star Schema → SQL Analysis → Power BI Visualization

### Data Sources
1. **Purchase Records** (CSV) - Transactional data
2. **Customer Information** (Excel) - Demographic data
3. **Customer Relations** (JSON) - Behavioral data

---

##  Project Structure
```text
BI-Customer-Behavior-Analysis/
├── scripts/
│ ├── extract.py # Data extraction functions
│ ├── transform.py # Data cleaning and transformation
│ ├── load.py # Database creation and loading
│ └── ROLAP_customer_Behavior.py # SQL analysis queries
├── data/
│ ├── raw data/ # Original data files
│ └── final data/ # Processed data files
├── documentation/
│ └── star_schema.png # Database schema diagram
├── .gitignore # Git exclusion rules
├── requirements.txt # Project's dependencies
└── README.md # Project documentation
```
---


##  Technologies Used
- **Python 3.x**: Data processing and ETL
- **Pandas**: Data manipulation and cleaning
- **SQLite3**: Relational database management
- **SQL**: Data analysis and querying
- **Power BI**: Data visualization and dashboarding
- **Git**: Version control

---

##  Key Analyses Performed

### Customer Demographics Analysis
- Subscription status impact on purchasing patterns
- Gender-based purchasing behavior
- Generational buying preferences
- Location-based sales distribution

### Sales & Product Analysis
- Seasonal purchase trends
- Monthly sales performance
- Top-performing product categories
- Discount effectiveness analysis

### Behavioral Insights
- Customer segmentation by purchase frequency
- Review rating patterns
- Size and color preferences by category
- Customer lifetime value analysis





