# Parking Table Analysis Report

## Executive Summary

This report provides a comprehensive analysis of the parking allocation system based on data from the Excel file "Parking table.xlsx". The analysis reveals insights about parking utilization, employee allocation, and data quality.

## Key Findings

### 📊 Dataset Overview
- **Total Records**: 56 parking assignments
- **Data Completeness**: 98.2% for core fields
- **File Structure**: 5 columns with employee and vehicle information

### 🚗 Parking Utilization
- **Total Allocated Spots**: 53
- **Available Free Spots**: 27
- **Utilization Rate**: 66.2%
- **Total Parking Capacity**: 80 spots

### 📍 Parking Zone Distribution

| Zone | Allocated Spots | Percentage |
|------|-----------------|------------|
| Underground | 19 | 35.8% |
| Covered Parking | 15 | 28.3% |
| English Yard Small | 9 | 17.0% |
| English Yard Large | 6 | 11.3% |
| Printing Area | 2 | 3.8% |
| Depot | 2 | 3.8% |

### 👥 Employee & Vehicle Analysis
- **Total Employees with Parking**: 56
- **Company Vehicles**: 3 (5.4%)
- **Personal Vehicles**: 53 (94.6%)

### 🚙 Vehicle Registration Types
- **Bulgarian License Plates**: 12 vehicles
- **Foreign License Plates**: 47 vehicles
- **Mixed/Multiple Plates**: 21 vehicles

### 🆓 Available Parking Spots by Zone
- Underground: 9 free spots
- Covered: 6 free spots
- English Yard Large: 2 free spots
- Entrance Alley: 2 free spots
- Depot: 2 free spots
- English Yard Small: 1 free spot
- Printing Area: 1 free spot

## Data Quality Assessment

### ✅ Strengths
- High data completeness (98.2%) for essential fields
- Consistent naming conventions for employee names (Cyrillic)
- Structured location coding system

### ⚠️ Areas for Improvement
- **Missing Data**: 51.8% of "Free" column entries are missing
- **Redundant Column**: "Unnamed: 3" column is 98.2% empty
- **Inconsistent Formatting**: Mixed Cyrillic and Latin characters in location names

## Parking Sector Analysis

The parking system uses a letter-number coding system:
- **Sector А**: 31 spots (largest sector)
- **Sector A**: 11 spots
- **Sector В**: 6 spots
- **Sector B**: 4 spots
- **Sector С**: 2 spots

*Note: There appears to be duplicate coding with both Cyrillic and Latin letters*

## Recommendations

### 1. Immediate Actions
- **Clean Data**: Remove or repurpose the mostly empty "Unnamed: 3" column
- **Complete Records**: Fill in missing "Free" spot assignments (29 missing entries)
- **Standardize Coding**: Unify parking sector naming (choose either Cyrillic or Latin)

### 2. System Improvements
- **Digital System**: Implement a parking management software
- **Real-time Tracking**: Enable dynamic spot allocation and availability tracking
- **Standardization**: Create consistent naming conventions across all fields

### 3. Capacity Planning
- Current utilization of 66.2% suggests adequate capacity
- Underground parking is most utilized (35.8% of allocated spots)
- Consider redistribution if certain zones become overcrowded

### 4. Data Management
- Regular data audits to maintain quality
- Backup and version control for parking assignments
- Integration with HR systems for automatic updates

## Technical Implementation

### Generated Files
1. `parking_analysis_summary.txt` - Basic data structure analysis
2. `parking_insights.txt` - Key metrics and insights
3. `parking_data_cleaned.csv` - Cleaned dataset for further analysis
4. `parking_analysis_dashboard.png` - Visual dashboard
5. `parking_sectors_analysis.png` - Sector distribution chart

### Tools Used
- **Python 3** with pandas, matplotlib, seaborn
- **Excel file processing** with openpyxl
- **Data visualization** and statistical analysis

## Conclusion

The parking allocation system appears well-managed with reasonable utilization rates. The main opportunities lie in data quality improvements and system standardization. The underground and covered parking areas are most popular, which aligns with expected preferences for protected parking.

The analysis suggests the organization has sufficient parking capacity for current needs, with room for expansion if required. Focus should be on improving data consistency and implementing digital management tools for better efficiency.

---

*Report generated on October 23, 2025*
*Analysis tools: Python, pandas, matplotlib, seaborn*