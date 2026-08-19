# ⬡ DataLens — Data Profiler & Schema Assistant

A lightweight Python + Streamlit tool that automatically analyzes raw CSV datasets, flags data quality issues, detects outliers, and generates production-ready SQL schema scripts — all in seconds.

---

## 🚀 Live Demo

👉 **[data-profiler-tool.streamlit.app](https://data-profiler-tool.streamlit.app)**

---

## ✨ Features

- 📊 **Automatic Data Profiling** — detects data types, row/column counts, and missing values instantly
- 🔍 **Outlier Detection** — flags numerical anomalies using the IQR (Interquartile Range) method
- 🗄️ **SQL Schema Generator** — suggests a clean relational schema and generates ready-to-run `CREATE TABLE` DDL scripts
- 📁 **Multi-format Support** — works with CSV files out of the box
- 🎨 **Clean Dark UI** — built with a custom Streamlit design system

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core application logic |
| Streamlit | Web interface |
| Pandas | Data profiling & transformation |
| SQLAlchemy | SQL script generation |

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Omer684/data-profiler-tool.git
cd data-profiler-tool
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## 📂 Project Structure

```
data-profiler-tool/
│
├── app.py              # Streamlit UI & main application
├── profiler.py         # Core profiling logic (DataProfiler class)
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 🔄 How It Works

```
User uploads CSV
       ↓
Pandas reads & analyzes the file
       ↓
Missing values → flagged per column
Outliers       → detected via IQR method
Data types     → inferred automatically
       ↓
Clean SQL schema → generated & displayed
       ↓
User copies SQL script → runs in any database
```

---

## 📦 Requirements

```
streamlit
pandas
sqlalchemy
```

---

## 🗺️ Roadmap

- [ ] JSON and SQL dump file support
- [ ] Export profiling report as PDF
- [ ] PostgreSQL / BigQuery direct connection
- [ ] Scheduled profiling with Apache Airflow
- [ ] Data cleaning suggestions with one-click fix

---

## 👤 Author

**Muhammad Omer**
- GitHub: [@Omer684](https://github.com/Omer684)
- LinkedIn: [your-linkedin-url]

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
