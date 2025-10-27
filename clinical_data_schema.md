# Unified Clinical Health Data Schema

## Overview
This schema provides a comprehensive, physician-focused view of patient health data aggregated from multiple wearable devices. It's designed for annual check-ups, clinical decision support, and LLM integration.

## Sample Data Table

| Date | Patient ID | Data Quality | Resting HR | HRV | Glucose | TIR | Weight | BMI | Sleep Hours | Recovery | Cognitive Readiness | Cardiovascular Risk | Metabolic Risk | Neurological Risk | Skeletal Risk |
|------|------------|--------------|------------|-----|---------|-----|--------|-----|-------------|----------|-------------------|-------------------|----------------|------------------|---------------|
| 2025-10-21 | 001 | 94.2% | 68 bpm | 47.2 ms | 112 mg/dL | 78.5% | 69.4 kg | 21.9 | 7.2 hrs | 52% | 74 | No abnormality suspected | No abnormality suspected | No abnormality suspected | No abnormality suspected |
| 2025-10-22 | 001 | 96.1% | 65 bpm | 52.1 ms | 108 mg/dL | 82.3% | 69.2 kg | 21.8 | 7.8 hrs | 68% | 78 | No abnormality suspected | No abnormality suspected | No abnormality suspected | No abnormality suspected |
| 2025-10-23 | 001 | 92.8% | 72 bpm | 41.3 ms | 125 mg/dL | 71.2% | 69.6 kg | 22.0 | 6.9 hrs | 45% | 65 | No abnormality suspected | Abnormality suspected | No abnormality suspected | No abnormality suspected |
| 2025-10-24 | 001 | 98.5% | 70 bpm | 48.7 ms | 115 mg/dL | 76.8% | 69.3 kg | 21.9 | 7.5 hrs | 58% | 71 | No abnormality suspected | No abnormality suspected | No abnormality suspected | No abnormality suspected |
| 2025-10-25 | 001 | 89.3% | 75 bpm | 38.9 ms | 142 mg/dL | 65.4% | 69.8 kg | 22.1 | 6.2 hrs | 38% | 58 | Abnormality suspected | Abnormality suspected | Abnormality suspected | No abnormality suspected |

### Key Observations from Sample Data:
- **Day 1-2**: Normal health parameters across all systems
- **Day 3**: Metabolic concern (high glucose, low TIR) - "Abnormality suspected"
- **Day 4**: Recovery trend observed
- **Day 5**: Multiple system concerns (cardiovascular, metabolic, neurological) - "Abnormality suspected"

### Clinical Interpretation:
- **Trend Analysis**: Declining health trajectory over 5 days
- **Risk Escalation**: Multiple systems showing abnormalities by Day 5
- **Action Required**: Physician consultation recommended for Days 3 and 5
- **Data Quality**: Generally high (89-98%) enabling reliable clinical assessment


## Clinical Risk Score Definitions

### Cardiovascular Risk Score
- **"No abnormality suspected"**: HRV >40ms, resting HR 50-80 bpm, stable trends, good recovery
- **"Abnormality suspected"**: HRV <30ms, resting HR >100 bpm, declining trends, poor recovery, irregular patterns

### Neurological Risk Score  
- **"No abnormality suspected"**: Cognitive scores >70, good focus, low stress, normal circadian compliance
- **"Abnormality suspected"**: Cognitive scores <50, poor focus, high stress, circadian disruption, declining trends

### Metabolic Risk Score
- **"No abnormality suspected"**: TIR >70%, GMI <5.7%, stable glucose, normal weight trends
- **"Abnormality suspected"**: TIR <60%, GMI >6.5%, high glucose variability, weight gain trend

### Skeletal Risk Score
- **"No abnormality suspected"**: Stable bone mass, adequate muscle mass, good body composition
- **"Abnormality suspected"**: Declining bone mass, muscle loss, poor body composition trends

## Detailed Field Definitions

### 1. Cardiovascular Health
- `avg_resting_hr_bpm`: Daily average resting heart rate
- `avg_hrv_ms`: Daily average heart rate variability (RMSSD)
- `hrv_trend`: 7-day HRV trend (improving/stable/declining)
- `cardiac_index`: Cardiac output index (from Starfit)
- `blood_pressure_systolic/diastolic`: If available from other sources

### 2. Metabolic Health
- `avg_glucose_mg_dl`: Daily average glucose
- `time_in_range_pct`: % time glucose 70-180 mg/dL
- `gmi_percent`: Glucose Management Indicator (HbA1c estimate)
- `glucose_variability_cv`: Coefficient of variation
- `insulin_sensitivity_index`: Derived metric from glucose patterns

### 3. Body Composition
- `weight_kg`: Daily weight
- `bmi`: Body mass index
- `body_fat_pct`: Body fat percentage
- `muscle_mass_kg`: Skeletal muscle mass
- `visceral_fat_level`: Visceral fat assessment
- `bone_mass_kg`: Bone density proxy
- `body_water_pct`: Hydration status

### 4. Sleep & Recovery
- `sleep_duration_hours`: Total sleep time
- `sleep_efficiency_pct`: % time in bed spent sleeping
- `sleep_consistency_pct`: Sleep schedule consistency
- `deep_sleep_pct`: % deep sleep
- `rem_sleep_pct`: % REM sleep
- `sleep_debt_hours`: Accumulated sleep deficit
- `recovery_score_pct`: Overall recovery from WHOOP

### 5. Cognitive & Neurological
- `cognitive_readiness_score`: Overall cognitive readiness (Pison)
- `mental_agility_score`: Cognitive processing speed
- `focus_score`: Attention and concentration
- `stress_level`: EDA-based stress measurement
- `circadian_compliance_pct`: Biological rhythm adherence

### 6. Activity & Fitness
- `daily_strain_score`: WHOOP strain score
- `energy_expenditure_kcal`: Daily calories burned
- `steps_count`: Daily step count
- `exercise_duration_min`: Active exercise time
- `cardio_fitness_score`: Derived cardiovascular fitness

### 7. Vital Signs
- `skin_temperature_celsius`: Core temperature proxy
- `blood_oxygen_pct`: Oxygen saturation
- `respiratory_rate_rpm`: Breathing rate

### 8. Clinical Risk Scores
- `cardiovascular_risk_score`: "No abnormality suspected" / "Abnormality suspected"
- `neurological_risk_score`: "No abnormality suspected" / "Abnormality suspected"
- `metabolic_risk_score`: "No abnormality suspected" / "Abnormality suspected"
- `skeletal_risk_score`: "No abnormality suspected" / "Abnormality suspected"

### 9. Clinical Indicators
- `inflammation_markers`: Derived from HRV patterns
- `oxidative_stress_level`: Derived from recovery patterns
- `autonomic_balance_score`: Parasympathetic/sympathetic balance
- `metabolic_age`: Biological age vs chronological age

### 10. Trend Analysis
- `*_trend_30d`: 30-day trends for key metrics
- Enables identification of health trajectory changes

### 11. Data Quality & Completeness
- `data_quality_score`: Overall data reliability (0-100%)
- `*_data_pct`: Percentage of expected data available per source

## Sample Unified Daily Record

```csv
date,patient_id,data_quality_score,avg_resting_hr_bpm,avg_hrv_ms,hrv_trend,cardiac_index,avg_glucose_mg_dl,time_in_range_pct,gmi_percent,glucose_variability_cv,weight_kg,bmi,body_fat_pct,muscle_mass_kg,visceral_fat_level,sleep_duration_hours,sleep_efficiency_pct,sleep_consistency_pct,deep_sleep_pct,rem_sleep_pct,sleep_debt_hours,recovery_score_pct,cognitive_readiness_score,mental_agility_score,focus_score,stress_level,circadian_compliance_pct,daily_strain_score,energy_expenditure_kcal,steps_count,exercise_duration_min,skin_temperature_celsius,blood_oxygen_pct,respiratory_rate_rpm,cardiovascular_risk_score,neurological_risk_score,metabolic_risk_score,skeletal_risk_score,inflammation_markers,oxidative_stress_level,autonomic_balance_score,metabolic_age,weight_trend_30d,glucose_trend_30d,hrv_trend_30d,sleep_trend_30d,recovery_trend_30d,whoop_data_pct,dexcom_data_pct,pison_data_pct,starfit_data_pct,elitehrv_data_pct,physician_notes,patient_reported_symptoms,medication_changes,life_events
2025-10-21,patient_001,94.2,68,47.2,stable,2.8,112,78.5,5.5,21.3,69.4,21.9,11.0,58.6,5.1,7.2,92,75,18.2,22.1,0.7,52,74,78,82,2.1,88,15.1,2345,6789,45,36.2,95.8,15.7,No abnormality suspected,No abnormality suspected,No abnormality suspected,No abnormality suspected,low,moderate,balanced,22,stable,stable,improving,stable,declining,98,96,87,100,85,Good overall health,None,None,Work stress
```

## FDA Compliance Considerations

### FDA Approval Required (Medical Device)
- **Diagnostic Claims**: "This device diagnoses diabetes" or "Detects heart disease"
- **Treatment Recommendations**: "Take medication X" or "See cardiologist immediately"
- **Medical Decision Making**: Device makes clinical decisions without physician oversight
- **High-Risk Conditions**: Life-threatening conditions (heart attack, stroke, diabetes)

### No FDA Approval Required (Wellness Device)
- **General Wellness**: "Track your fitness" or "Monitor your sleep"
- **Educational Information**: "Learn about your health patterns"
- **Lifestyle Suggestions**: "Consider more exercise" or "Try better sleep hygiene"
- **Data Presentation**: Raw data without clinical interpretation

### Compliance Strategies
1. **Clear Disclaimers**: "This tool is for informational purposes only"
2. **Physician Oversight**: All clinical decisions made by licensed physicians
3. **Educational Language**: Focus on "patterns" and "trends" rather than "diagnoses"
4. **Referral Language**: "Consider discussing with your physician" vs "You have diabetes"

## Implementation Notes

### Data Aggregation Strategy
- **Daily Averages**: All metrics aggregated to daily level
- **Trend Analysis**: 30-day moving averages for trend detection
- **Quality Scoring**: Data completeness and reliability assessment
- **Risk Scoring**: Clinical risk assessment with physician oversight

### LLM Integration
- **Structured Format**: Easy for AI to parse and analyze
- **Comprehensive Coverage**: All major health domains included
- **Trend Analysis**: Longitudinal data for pattern recognition
- **Clinical Context**: Physician notes and patient symptoms included

### Physician Benefits
- **Holistic View**: Single dashboard for all health metrics
- **Risk Stratification**: Clear cardiovascular, metabolic, and cognitive risk indicators
- **Trend Analysis**: 30-day trends show health trajectory
- **Clinical Decision Support**: Data-driven insights for patient care