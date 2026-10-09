

# 🌪️ DisasterGuard AI

### 🚨 AI-Powered Multi-Hazard Disaster Risk Monitoring & Safe Route Assistant

<p align="center">
  <img src="https://img.shields.io/badge/AI%20%26%20ML-Random%20Forest-8B5CF6?style=for-the-badge" alt="AI & ML">
  <img src="https://img.shields.io/badge/Weather-Live%20Intelligence-06B6D4?style=for-the-badge" alt="Weather">
  <img src="https://img.shields.io/badge/Maps-Leaflet%20%2B%20OSM-22C55E?style=for-the-badge" alt="Maps">
  <img src="https://img.shields.io/badge/Routing-OSRM-F97316?style=for-the-badge" alt="Routing">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20App-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Scikit--learn-Machine%20Learning-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/OpenStreetMap-Mapping-7EBC6F?style=flat-square&logo=openstreetmap&logoColor=white" alt="OpenStreetMap">
</p>

<p align="center">
  🌦️ <b>Predict</b> • 🗺️ <b>Monitor</b> • 🤖 <b>Analyse</b> • 🚗 <b>Navigate</b> • 🛡️ <b>Stay Safe</b>
</p>

---

## 🌈 What is DisasterGuard AI?

**DisasterGuard AI** is a web-based disaster monitoring and decision-support platform designed to help users understand environmental risks and make safer travel decisions.

The project combines:

* 🤖 Machine Learning for flood-risk prediction
* 🌦️ Live weather intelligence
* 📚 Historical disaster analysis
* 🗺️ Interactive multi-hazard mapping
* ⚡ Lightning risk analysis
* 🌪️ Storm and severe-weather monitoring
* 🚗 Safe route analysis
* 🛣️ Alternative route comparison
* 🚨 Emergency and safety guidance
* 📍 Location-based monitoring

Instead of showing only weather information, DisasterGuard AI combines multiple hazard indicators into one dashboard and presents them in an easy-to-understand safety view.

> ⚠️ **Important:** DisasterGuard AI is an educational, research and hackathon prototype. It should not be treated as an official emergency-warning or life-safety system.

---

# ✨ Key Features

| Feature                    | Description                                                   |
| -------------------------- | ------------------------------------------------------------- |
| 🌦️ Weather Intelligence   | Monitors current weather and environmental conditions.        |
| 🌊 AI Flood Prediction     | Uses a Random Forest model for flood-risk prediction.         |
| ⚡ Lightning Risk           | Provides lightning-related risk information.                  |
| 🌪️ Storm Risk             | Analyses storm and severe-weather conditions.                 |
| 🗺️ Multi-Hazard Risk Map  | Displays disaster-related information on an interactive map.  |
| 📚 Historical Risk         | Analyses historical disaster records for a selected city.     |
| 🚗 Safe Route Analysis     | Analyses travel risk for a selected destination.              |
| 🛣️ Route Comparison       | Compares available driving routes based on risk exposure.     |
| 🚨 Emergency Action Center | Provides emergency-oriented safety assistance.                |
| 🏥 Nearby Help             | Supports access to hospitals, shelters and police assistance. |
| 📊 Smart Dashboard         | Displays risk cards, alerts, maps and safety information.     |
| 📍 Location Monitoring     | Allows monitoring of a selected geographical location.        |

---

# 🤖🧠 Artificial Intelligence

## Random Forest Flood-Risk Prediction

DisasterGuard AI includes a **Random Forest Classifier** for flood-risk prediction.

### Model Inputs

The current trained model uses:

* `Temperature`
* `Rainfall`
* `Max_Wind`

### Target

* `Flood`

### Example Prediction

```json
{
  "prediction": 1,
  "result": "FLOOD RISK",
  "probability": 78.4
}
```

A normal-risk example:

```json
{
  "prediction": 0,
  "result": "NORMAL",
  "probability": 12.5
}
```

### 🧪 Model Training Process

The training script:

1. Loads `data/ml_dataset.csv`
2. Selects `Temperature`, `Rainfall`, and `Max_Wind`
3. Splits the dataset into training and testing sets
4. Trains a `RandomForestClassifier`
5. Evaluates the model using accuracy and classification report
6. Saves the trained model

Model output:

```text
models/flood_model.pkl
```

### ML Pipeline

```text
Historical Dataset
       ↓
Data Preparation
       ↓
Feature Selection
       ↓
Train / Test Split
       ↓
Random Forest Training
       ↓
Model Evaluation
       ↓
flood_model.pkl
       ↓
Flask API
       ↓
Web Dashboard
```

---

# 📊 Dataset & Historical Intelligence

The project contains multiple datasets used for machine learning, weather analysis and disaster-risk monitoring.

## Main ML Dataset

```text
data/ml_dataset.csv
```

Current dataset:

* **4,228 records**
* **9 columns**

Important fields:

| Field       | Purpose                 |
| ----------- | ----------------------- |
| Date        | Observation date        |
| District    | District name           |
| State       | State name              |
| Latitude    | Geographic latitude     |
| Longitude   | Geographic longitude    |
| Temperature | Temperature value       |
| Rainfall    | Rainfall value          |
| Max_Wind    | Maximum wind speed      |
| Flood       | Flood prediction target |

## Historical Weather Dataset

```text
data/historical_weather_dataset.csv
```

Contains historical weather records prepared for project analysis.

## Flood / Disaster Dataset

```text
data/flood_data.csv
```

Contains historical flood/disaster information such as:

* Date
* Location
* District
* State
* Latitude
* Longitude
* Severity
* Area affected
* Human casualties
* Damage information
* Event source

## Historical Disaster Records

```text
data/historical_disasters.json
```

These records are used for historical disaster-risk analysis.

---

# 🔬 Historical Risk Analysis

DisasterGuard AI provides a dedicated historical-risk API.

### API

```text
GET /historical-risk?city=<city>
```

The application analyses stored disaster records for the requested city.

It considers:

* Number of incidents
* High-severity incidents
* Medium-severity incidents

The result is converted into:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Historical risk provides additional context alongside current environmental conditions.

---

# 🌦️ Live Weather Intelligence

The dashboard uses live weather information to support current risk assessment.

The frontend connects to **Open-Meteo** for weather and forecast information.

The system considers environmental signals related to:

* 🌧️ Rainfall
* 🌡️ Temperature
* 💨 Wind
* ⚡ Lightning
* 🌪️ Storm
* ⛈️ Severe Weather

Weather information is combined with the project's risk-analysis logic to provide understandable hazard information.

---

# ⚡ Lightning Risk Analysis

DisasterGuard AI analyses environmental conditions related to potential lightning risk.

The dashboard can display statuses such as:

* 🟢 **LOW RISK**
* 🟡 **CAUTION**
* 🟠 **HIGH RISK**
* 🔴 **CRITICAL**

---

# 🌪️ Storm & Severe Weather Monitoring

The platform monitors multiple environmental hazards including:

* 🌪️ Storms
* 💨 Strong Winds
* ⛈️ Severe Weather
* 🌧️ Heavy Rainfall
* ⚡ Lightning

This allows the system to consider multiple hazards instead of focusing only on floods.

---

# 🗺️ Interactive Multi-Hazard Risk Map

The dashboard contains an interactive map powered by:

* **Leaflet**
* **OpenStreetMap**

The map can display:

* 📍 Monitoring location
* 🌊 Flood-risk information
* ⚡ Lightning-risk information
* 🌪️ Storm information
* 🛣️ Route alternatives
* 🟢 Recommended routes
* ⚠️ Hazard information

The map makes complex disaster-risk information easier to understand visually.

---

# 🚗 Safe Route Analysis

One of the main features of DisasterGuard AI is **Safe Route Analysis**.

Users can provide a destination and the system analyses the current environmental risk.

The analysis considers:

* Overall risk
* Flood risk
* Lightning risk
* Storm risk
* Severe weather risk

The system can generate:

```text
🟢 LOW RISK
🟡 CAUTION
🟠 HIGH RISK
🔴 CRITICAL
```

It also provides a human-readable recommendation.

### Example

```text
High Flood Risk detected.

Avoid unnecessary travel and high-risk areas.

Avoid waterlogged roads, drainage areas
and low-lying locations.
```

---

# 🧭 Alternative Route Comparison

The `/compare-routes` endpoint provides route comparison.

### How It Works

```text
Your Location
      ↓
Destination Geocoding
      ↓
Driving Route Generation
      ↓
Route Distance Calculation
      ↓
Environmental Risk Analysis
      ↓
Route Risk Comparison
      ↓
Safer Route Recommendation
```

### Technologies Used

* **Nominatim / OpenStreetMap** — destination geocoding
* **OSRM** — driving-route generation
* **Project hazard-risk values** — route exposure analysis

Route results can include:

* Distance
* Estimated duration
* Risk level
* Safety status
* Recommendation
* Route geometry

---

# 🚨 Emergency Action Center

The platform includes an Emergency Action Center to provide quick access to safety-oriented assistance.

Possible assistance includes:

* 🏥 Nearby hospitals
* 🚓 Police assistance
* 🛟 Shelters
* 📞 Emergency services
* 📍 Nearby help
* 🗺️ Navigation support

The objective is to bring useful emergency resources together in one place.

---

# 🔄 How DisasterGuard AI Works

```text
                 🌦️ Weather Data
                       │
                       ▼
            ┌─────────────────────┐
            │ Environmental Risk  │
            │     Processing      │
            └──────────┬──────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      🌊 Flood     ⚡ Lightning   🌪️ Storm
          │            │            │
          └────────────┼────────────┘
                       ▼
                📊 Overall Risk
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   🤖 ML Flood Model        📚 Historical Data
          │                         │
          └────────────┬────────────┘
                       ▼
              🛡️ DisasterGuard AI
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      🗺️ Risk Map   🚗 Safe Route  🚨 Safety
```

---

# 🖥️ Smart Disaster Dashboard

The web dashboard works as a lightweight disaster-monitoring center.

### Main Dashboard Sections

* 🛡️ Current Safety Status
* 🌦️ Weather Risk
* 🌊 Flood Risk
* ⚡ Lightning Risk
* 🌪️ Storm Risk
* 🗺️ Multi-Hazard Risk Map
* 🔮 Risk Prediction
* ❓ Why This Risk?
* 📚 Historical vs Current Risk
* 🚗 Safe Route
* 🚨 Emergency Help
* 🆘 Safety Instructions
* 📍 Emergency Action Center

The interface combines risk cards, maps, alerts and visual indicators into one dashboard.

---

# 🧩 Technology Stack

## Backend

* 🐍 Python
* 🌐 Flask
* 📦 Joblib

## Machine Learning

* 🤖 Scikit-learn
* 🌲 Random Forest
* 🐼 Pandas
* 🔢 NumPy

## Frontend

* HTML5
* CSS3
* JavaScript
* Leaflet.js

## Maps & Routing

* 🗺️ OpenStreetMap
* 📍 Nominatim
* 🛣️ OSRM

## Weather

* 🌦️ Open-Meteo

---

# 📁 Project Structure

```text
DISASTERGUARD_AI/
│
├── app.py
├── train_model.py
├── prepare_dataset.py
├── check_dataset.py
├── check_historical_weather_dataset.py
├── clean_district_list.py
├── clean_flood_data.py
├── create_normal_samples.py
├── district_list.py
├── get_district_coordinates.py
├── historical_weather_batch_test.py
├── historical_weather_dataset.py
├── historical_weather_test.py
├── inspect_weather_data.py
│
├── data/
│   ├── ml_dataset.csv
│   ├── historical_weather_dataset.csv
│   ├── flood_data.csv
│   ├── flood_cleaned.csv
│   ├── disaster_ml_dataset.csv
│   ├── historical_disasters.json
│   ├── district_coordinates.csv
│   ├── district_coordinates_test.csv
│   └── district_list_cleaned.csv
│
├── models/
│   └── flood_model.pkl
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── dashboard.js
│
├── templates/
│   └── index.html
│
├── database/
│
├── requirements.txt
│
└── README.md
```

> 💡 **Note:** Do not commit your local `venv/` directory to GitHub. Create a fresh virtual environment locally.

---

# 🚀 Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Krisha933/DISASTERGUARD_AI.git
cd DISASTERGUARD_AI
```

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install flask pandas numpy scikit-learn joblib
```

Or, if `requirements.txt` is complete:

```bash
pip install -r requirements.txt
```

After confirming the project works, update the requirements file:

```bash
pip freeze > requirements.txt
```

---

# 🤖 Train the Flood Model

To retrain the Random Forest model:

```bash
python train_model.py
```

The script reads:

```text
data/ml_dataset.csv
```

and saves the trained model to:

```text
models/flood_model.pkl
```

---

# ▶️ Run the Application

From the project root:

```bash
python app.py
```

The Flask application normally runs at:

```text
http://127.0.0.1:5000
```

or:

```text
http://localhost:5000
```

Open the address in your browser.

---

# 🔌 Main API Endpoints

| Endpoint               | Purpose                               |
| ---------------------- | ------------------------------------- |
| `GET /`                | Loads the DisasterGuard AI dashboard  |
| `GET /predict-flood`   | Predicts flood risk                   |
| `GET /historical-risk` | Calculates historical disaster risk   |
| `GET /safe-route`      | Analyses destination travel risk      |
| `GET /compare-routes`  | Finds and compares alternative routes |
| `GET /geocode`         | Geocodes a location                   |

### Flood Prediction Example

```text
/predict-flood?temperature=30&rainfall=120&wind=25
```

### Historical Risk Example

```text
/historical-risk?city=Lucknow
```

---

# 🌐 External Services

| Service           | Purpose                   |
| ----------------- | ------------------------- |
| 🌦️ Open-Meteo    | Weather and forecast data |
| 🗺️ OpenStreetMap | Map data                  |
| 📍 Nominatim      | Destination geocoding     |
| 🛣️ OSRM          | Driving route generation  |
| 🧭 Google Maps    | Navigation/search links   |

External services may have their own availability, usage limits and terms.

---

# 🎯 Real-World Applications

DisasterGuard AI demonstrates how technology could support:

### 🏙️ Smart Cities

Monitor environmental conditions and present location-based risk information.

### 🚗 Safer Travel

Help users understand whether current environmental conditions may make a journey risky.

### 🏫 Educational Institutions

Demonstrate the practical use of:

* Machine Learning
* APIs
* Maps
* Data analysis
* Web development

### 🚨 Disaster Awareness

Present multiple hazard indicators and safety recommendations through one interface.

### 🏢 Emergency Planning

Provide a prototype dashboard for studying multi-hazard monitoring workflows.

### 🗺️ Location-Based Risk Analysis

Combine geographic, weather and historical information for a selected area.

---

# 🏆 Why This Project Is Different

DisasterGuard AI is not just a simple weather application.

It combines:

```text
🤖 MACHINE LEARNING
        +
🌦️ WEATHER DATA
        +
📚 HISTORICAL DATA
        +
⚠️ RISK ANALYSIS
        +
🗺️ INTERACTIVE MAP
        +
🛣️ ROUTE COMPARISON
        +
🚨 SAFETY GUIDANCE
        ↓
🛡️ DISASTERGUARD AI
```

This makes the project suitable for:

* 🏆 Hackathons
* 🎓 College projects
* 🤖 AI/ML demonstrations
* 🌍 Disaster-management concepts
* 💻 Full-stack web development projects

---

# 📊 Current Capabilities

### Phase 1 — Core Intelligence

* ✅ AI flood prediction
* ✅ Random Forest model
* ✅ Live weather monitoring
* ✅ Historical disaster analysis
* ✅ Interactive risk mapping

### Phase 2 — Advanced Intelligence

* ✅ Lightning risk analysis
* ✅ Storm risk analysis
* ✅ Severe weather analysis
* ✅ Safe route analysis
* ✅ Alternative route comparison
* ✅ Location-based monitoring
* ✅ Real-time map information

### Phase 3 — Emergency & Safety

* ✅ Emergency Action Center
* ✅ Nearby hospitals
* ✅ Police assistance
* ✅ Shelter information
* ✅ Safe-zone identification
* ✅ Emergency-service support
* ✅ Multi-hazard monitoring
* ✅ Community-oriented disaster assistance

These capabilities represent the current project implementation and are not listed as future-only features.

---

# ⚠️ Limitations

The current project is a prototype and has important limitations:

* The flood model uses a limited set of input features.
* Historical disaster data is limited compared with real-world disaster databases.
* ML predictions can produce false positives or false negatives.
* A model probability is not proof that a disaster will occur.
* Route risk is an estimation based on available hazard values and route exposure.
* External APIs depend on network connectivity and third-party availability.
* Geographic coverage may vary depending on available data.
* The project is not an official government emergency-warning system.

A production-grade system would require:

* Reliable real-time disaster data
* Stronger model validation
* Authentication
* Logging
* Monitoring
* Better data pipelines
* Scalable infrastructure
* Official emergency-data integrations

---

# 🔮 Future Improvements

Possible future enhancements include:

* 🧠 Advanced Deep Learning models
* 🌊 More advanced flood forecasting
* 🛰️ Satellite imagery integration
* 📡 IoT sensor integration
* 📍 Real-time GPS tracking
* 🚨 SMS / Email / Push notifications
* 📱 Dedicated Android/iOS application
* 🗄️ Database-backed event history
* 👤 User authentication
* 🧭 Advanced route-risk scoring
* 🗺️ Live flood-zone overlays
* 🔥 Wildfire and heatwave prediction
* 🌍 Additional disaster categories
* 📈 Historical trend analytics
* ☁️ Cloud deployment
* 🐳 Docker support
* 🧪 Automated ML model evaluation
* 💡 Explainable AI for predictions

---

# 🔐 Safety & Responsible Use

DisasterGuard AI is designed for educational, research, hackathon and safety-awareness purposes.

**Do not rely on this prototype as the sole source of information during an actual emergency.**

During a real disaster, always follow instructions from:

* Government authorities
* Official disaster-management agencies
* Local emergency services
* Official weather authorities

---

# 👩‍💻 Developer

**Krisha Singh**

**B.Tech Computer Science & Engineering**

🌪️ **DisasterGuard AI**

GitHub:
[https://github.com/Krisha933](https://github.com/Krisha933)

---

# 📜 License

This project is intended for educational and research purposes.

If you want others to legally use, modify and distribute the project, consider adding an open-source license such as the **MIT License**.

---

# ⭐ Conclusion

DisasterGuard AI demonstrates how Machine Learning, weather intelligence, historical disaster data, interactive maps and route analysis can be combined into a single disaster-risk monitoring platform.

```text
🌦️ Environmental Monitoring
          ↓
🤖 ML Flood Prediction
          ↓
📚 Historical Risk Analysis
          ↓
🗺️ Multi-Hazard Visualization
          ↓
🚗 Safe Route Analysis
          ↓
🚨 Safety Recommendations
```

## 🎯 Project Goal

> **Make disaster-related information easier to understand and demonstrate how AI and modern web technologies can support smarter, safer and more informed decision-making.**

---

<p align="center">

## 🛡️ DisasterGuard AI

### Predict • Monitor • Analyse • Navigate • Stay Safe

Made with ❤️ for AI, ML & Disaster-Safety Innovation

</p>
