# Harmona: Health Data Harmonization Project

## Overview

Harmona is a comprehensive health data harmonization platform designed to integrate, standardize, and analyze multi-source health monitoring data for clinical insights. The project aims to create a unified data schema that enables physicians to gain comprehensive insights from diverse health monitoring devices.

## Current Data Sources

### ✅ Available Data
- **WHOOP** - Comprehensive physiological monitoring
  - `physiological_cycles.csv` - Daily recovery, HRV, sleep metrics
  - `sleeps.csv` - Detailed sleep analysis
  - `workouts.csv` - Exercise tracking and strain metrics
- **Starfit Smart Scale** - Body composition tracking
  - `Starfit-Tuck.csv` - Weight, BMI, body fat, muscle mass, etc.
- **EliteHRV via Polar** - Heart rate variability monitoring
  - `elitehrv_03292024.csv` - HRV readings, readiness scores, breathing patterns

### 🔄 Pending Data Sources
- **Pison EMG** - Electromyography data (muscle activity)
- **Dexcom** - Continuous glucose monitoring (or alternative CGM)

## Project Phases

### Phase 1: Data Collection & Sample Generation
**Goal**: Generate realistic sample data for missing sources

#### For Cursor AI Implementation:
```
Generate sample data for:
1. Pison EMG device - muscle activity patterns during different activities
2. Dexcom CGM - continuous glucose readings with meal/exercise correlations
```

**Sample Data Requirements:**
- **Pison EMG**: 30 days of data with muscle activity during sleep, exercise, daily activities
- **Dexcom CGM**: 30 days of glucose readings (every 5 minutes) with meal/exercise annotations

### Phase 2: Unified Data Schema Design
**Goal**: Create physician-friendly data structure

#### Proposed Schema Categories:
1. **Temporal Data** - All measurements with standardized timestamps
2. **Cardiovascular Metrics** - HR, HRV, blood pressure, recovery
3. **Metabolic Data** - Glucose, BMR, energy expenditure
4. **Body Composition** - Weight, BMI, muscle mass, body fat
5. **Sleep & Recovery** - Sleep stages, efficiency, consistency
6. **Activity & Exercise** - Strain, workouts, muscle activation
7. **Environmental Factors** - Timezone, notes, tags

### Phase 3: Data Harmonization
**Goal**: Transform all data sources into unified format

#### Harmonization Process:
1. **Timestamp Standardization** - Convert all timestamps to UTC
2. **Unit Conversion** - Standardize units (metric/imperial, time zones)
3. **Data Mapping** - Map device-specific fields to schema categories
4. **Quality Control** - Handle missing values, outliers, data validation
5. **Export Generation** - Create unified CSV with all harmonized data

### Phase 4: LLM Integration (Future)
**Goal**: AI-powered health insights and trend analysis

#### Planned Features:
- Trend analysis across health systems
- Correlation identification between metrics
- Personalized health recommendations
- Automated report generation for physicians

## Technical Implementation

### Data Structure
```
harmona/
├── data/
│   ├── whoop/           # WHOOP device data
│   ├── starfit/         # Smart scale data
│   ├── polar/           # EliteHRV data
│   ├── pison/           # EMG data (to be generated)
│   └── dexcom/          # CGM data (to be generated)
├── schema/              # Data schema definitions
├── harmonization/       # Data processing scripts
├── exports/             # Unified data exports
└── analysis/            # LLM integration (future)
```

### Key Data Fields Analysis

#### WHOOP Data (Most Comprehensive):
- **Recovery**: Recovery score, resting HR, HRV, skin temp, blood oxygen
- **Sleep**: Sleep stages, efficiency, consistency, respiratory rate
- **Activity**: Strain, energy burned, HR zones, GPS tracking

#### Starfit Data:
- **Body Composition**: Weight, BMI, body fat %, muscle mass, bone mass
- **Metabolic**: BMR, body age, protein %, body water %

#### EliteHRV Data:
- **HRV Metrics**: RMSSD, SDNN, frequency domain analysis
- **Readiness**: Morning readiness scores, balance indicators
- **Context**: Breathing patterns, position, notes

## Implementation Instructions for Cursor AI

### Step 1: Generate Sample Data
Create realistic sample data files for:

**Pison EMG Sample Data Structure:**
```csv
timestamp,muscle_group,activity_type,emg_amplitude,emg_frequency,activity_intensity,notes
2025-01-01 08:00:00,biceps,typing,12.5,45.2,low,desk work
2025-01-01 12:00:00,deltoids,exercise,89.3,78.1,high,weight training
```

**Dexcom CGM Sample Data Structure:**
```csv
timestamp,glucose_mg_dl,trend,meal_type,exercise_type,insulin_units,notes
2025-01-01 08:00:00,95,steady,breakfast,none,0,pre-meal
2025-01-01 10:30:00,145,rising,post-meal,cardio,0,post-workout
```

### Step 2: Define Unified Schema
Create a comprehensive data schema that maps all device data to standardized fields:

**Proposed Unified Schema:**
```csv
timestamp,data_source,metric_category,metric_name,value,unit,quality_score,context
2025-01-01 08:00:00,whoop,cardiovascular,heart_rate,65,bpm,0.95,resting
2025-01-01 08:00:00,starfit,body_composition,weight,152.8,lb,0.98,morning
```

### Step 3: Data Harmonization Script
Develop Python scripts to:
1. Read all CSV files from different sources
2. Map fields to unified schema
3. Handle data quality issues
4. Export harmonized dataset

### Step 4: Quality Assurance
- Validate data completeness
- Check for temporal consistency
- Ensure unit standardization
- Generate data quality reports

## Expected Outcomes

### For Physicians:
1. **Unified Dashboard** - Single view of all patient health metrics
2. **Trend Analysis** - Longitudinal health pattern identification
3. **Correlation Insights** - Understanding relationships between different health systems
4. **Clinical Decision Support** - Data-driven treatment recommendations

### For Patients:
1. **Comprehensive Health View** - Integration of all monitoring devices
2. **Personalized Insights** - AI-powered health recommendations
3. **Progress Tracking** - Long-term health trend monitoring

## Next Steps

1. **Immediate**: Generate sample data for Pison EMG and Dexcom CGM
2. **Short-term**: Implement data harmonization pipeline
3. **Medium-term**: Develop unified data export functionality
4. **Long-term**: Integrate LLM for automated health insights

## Data Privacy & Security

- All data processing should be done locally
- No health data should be transmitted to external services
- Implement proper data anonymization for research purposes
- Follow HIPAA guidelines for health data handling

## Contributing

This project is designed to be extensible. New data sources can be added by:
1. Creating sample data in the appropriate directory
2. Defining mapping rules to the unified schema
3. Adding harmonization logic to the processing pipeline

---

*This README serves as a comprehensive guide for implementing the Harmona health data harmonization platform. Each phase builds upon the previous one, creating a robust system for multi-source health data integration and analysis.*
