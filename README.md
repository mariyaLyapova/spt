# SPT - Smart Parking Tracker

A comprehensive parking management and analysis system designed to optimize parking allocation, track utilization, and provide detailed insights through interactive visualizations.

## 🚀 Features

- **Data Management**: Process and clean parking data from Excel files
- **Interactive Visualizations**: HTML-based parking spot visualizers and calendars
- **Analytics Engine**: Comprehensive parking utilization analysis and reporting
- **Registry Management**: Employee and vehicle registration tracking
- **Historical Data**: Track parking assignments over time
- **Multi-format Support**: JSON, CSV, and Excel data formats

## 📊 Key Capabilities

- **Real-time Parking Status**: Monitor occupied and available spots
- **Zone-based Analysis**: Analyze parking by different areas (Underground, Covered, English Yard, etc.)
- **Vehicle Registration Tracking**: Support for Bulgarian and foreign license plates
- **Utilization Reports**: Detailed statistics and trends
- **Data Quality Assessment**: Automated data validation and cleaning

## 🏗️ Project Structure

```
spt/
├── parking_calendar.html         # Interactive calendar view
├── parking_spots_visualizer.html # Visual parking layout
├── processor.py                  # Data consolidation script
├── requirements.txt              # Python dependencies
├── PARKING_ANALYSIS_REPORT.md    # Comprehensive analysis report
├── README.md                     # Project documentation
└── .gitignore                    # Git ignore rules
```

**Note**: This repository contains the core implementation. Input data, legacy code, and generated files are excluded for security and cleanliness.

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/spt.git
   cd spt
   ```

2. **Install dependencies**
   ```bash
   pip install -r new/requirements.txt
   ```

## 📖 Usage

### Data Processing
```bash
# Merge and process parking data (requires input data)
python processor.py
```

### Visualizations
Open the HTML files in your browser:
- `parking_spots_visualizer.html` - Interactive parking layout
- `parking_calendar.html` - Calendar-based view

### Analytics
Review the comprehensive analysis:
- `PARKING_ANALYSIS_REPORT.md` - Detailed insights and statistics

## 📈 Sample Insights

Based on current data analysis:
- **Total Parking Capacity**: 80 spots
- **Current Utilization**: 66.2%
- **Available Spots**: 27
- **Most Popular Zone**: Underground (35.8% allocation)
- **Vehicle Types**: 94.6% personal, 5.4% company vehicles

## 🔧 Configuration

The system processes parking data from Excel files placed in an input directory. Key components:
- Main processing script: `processor.py`
- Dependencies listed in: `requirements.txt`
- Analysis output: `PARKING_ANALYSIS_REPORT.md`

## 📊 Data Formats

**Supported Input Formats**:
- Excel (.xlsx) - Primary parking table format

**Output Formats**:
- JSON - Machine-readable data (generated locally)
- HTML - Interactive visualizations
- Markdown - Human-readable reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support:
- Create an issue in the GitHub repository
- Review the analysis reports for data insights
- Check the processing logs for troubleshooting

## 🔮 Roadmap

- [ ] Real-time parking updates
- [ ] Mobile-responsive visualizations
- [ ] API endpoints for external integrations
- [ ] Advanced predictive analytics
- [ ] Multi-language support
- [ ] Integration with parking sensors

---

*SPT - Making parking management smarter, one spot at a time.*