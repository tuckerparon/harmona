#!/usr/bin/env python3
"""
Data Harmonization Script for Multi-Device Health Data
Harmonizes WHOOP, Starfit, EliteHRV, Dexcom, and Pison data into unified clinical schema
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

class HealthDataHarmonizer:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.unified_schema = self._define_unified_schema()
        
    def _define_unified_schema(self):
        """Define the unified clinical data schema"""
        return [
            'date', 'patient_id', 'data_quality_score',
            # Cardiovascular Health
            'avg_resting_hr_bpm', 'avg_hrv_ms', 'hrv_trend', 'cardiac_index', 
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            # Metabolic Health
            'avg_glucose_mg_dl', 'time_in_range_pct', 'gmi_percent', 
            'glucose_variability_cv', 'insulin_sensitivity_index',
            # Body Composition
            'weight_kg', 'bmi', 'body_fat_pct', 'muscle_mass_kg', 
            'visceral_fat_level', 'bone_mass_kg', 'body_water_pct',
            # Sleep & Recovery
            'sleep_duration_hours', 'sleep_efficiency_pct', 'sleep_consistency_pct',
            'deep_sleep_pct', 'rem_sleep_pct', 'sleep_debt_hours', 'recovery_score_pct',
            # Cognitive & Neurological
            'cognitive_readiness_score', 'mental_agility_score', 'focus_score',
            'stress_level', 'circadian_compliance_pct',
            # Activity & Fitness
            'daily_strain_score', 'energy_expenditure_kcal', 'steps_count',
            'exercise_duration_min', 'cardio_fitness_score',
            # Vital Signs
            'skin_temperature_celsius', 'blood_oxygen_pct', 'respiratory_rate_rpm',
            # Clinical Risk Scores
            'cardiovascular_risk_score', 'neurological_risk_score', 
            'metabolic_risk_score', 'skeletal_risk_score',
            # Clinical Indicators
            'inflammation_markers', 'oxidative_stress_level', 'autonomic_balance_score',
            'metabolic_age',
            # Trend Indicators
            'weight_trend_30d', 'glucose_trend_30d', 'hrv_trend_30d',
            'sleep_trend_30d', 'recovery_trend_30d',
            # Data Completeness
            'whoop_data_pct', 'dexcom_data_pct', 'pison_data_pct',
            'starfit_data_pct', 'elitehrv_data_pct',
            # Clinical Notes
            'physician_notes', 'patient_reported_symptoms', 'medication_changes', 'life_events'
        ]
    
    def load_whoop_data(self):
        """Load and process WHOOP physiological cycles data"""
        try:
            df = pd.read_csv(f"{self.data_dir}/whoop/physiological_cycles.csv")
            
            # Parse dates and extract date only
            df['date'] = pd.to_datetime(df['Cycle start time']).dt.date
            
            # Group by date and calculate daily averages
            daily_data = df.groupby('date').agg({
                'Recovery score %': 'mean',
                'Resting heart rate (bpm)': 'mean',
                'Heart rate variability (ms)': 'mean',
                'Skin temp (celsius)': 'mean',
                'Blood oxygen %': 'mean',
                'Day Strain': 'mean',
                'Energy burned (cal)': 'sum',
                'Max HR (bpm)': 'max',
                'Average HR (bpm)': 'mean',
                'Sleep performance %': 'mean',
                'Respiratory rate (rpm)': 'mean',
                'Asleep duration (min)': 'sum',
                'In bed duration (min)': 'sum',
                'Light sleep duration (min)': 'sum',
                'Deep (SWS) duration (min)': 'sum',
                'REM duration (min)': 'sum',
                'Awake duration (min)': 'sum',
                'Sleep need (min)': 'mean',
                'Sleep debt (min)': 'mean',
                'Sleep efficiency %': 'mean',
                'Sleep consistency %': 'mean'
            }).reset_index()
            
            # Convert sleep durations to hours
            daily_data['sleep_duration_hours'] = daily_data['Asleep duration (min)'] / 60
            daily_data['deep_sleep_pct'] = (daily_data['Deep (SWS) duration (min)'] / 
                                          daily_data['Asleep duration (min)'] * 100)
            daily_data['rem_sleep_pct'] = (daily_data['REM duration (min)'] / 
                                         daily_data['Asleep duration (min)'] * 100)
            daily_data['sleep_debt_hours'] = daily_data['Sleep debt (min)'] / 60
            
            return daily_data
        except Exception as e:
            print(f"Error loading WHOOP data: {e}")
            return pd.DataFrame()
    
    def load_starfit_data(self):
        """Load and process Starfit smart scale data"""
        try:
            df = pd.read_csv(f"{self.data_dir}/starfit/Starfit-Tuck.csv")
            
            # Parse dates
            df['date'] = pd.to_datetime(df['Date']).dt.date
            
            # Clean and convert data
            df['Weight'] = df['Weight'].str.replace('lb', '').astype(float) * 0.453592  # Convert to kg
            df['BMI'] = df['BMI'].astype(float)
            df['Body Fat'] = df['Body Fat'].str.replace('%', '').astype(float)
            df['Heart Rate'] = df['Heart Rate'].str.replace('bpm', '').astype(float)
            df['Cardiac Index'] = df['Cardiac Index'].str.replace('L/Min/㎡', '').astype(float)
            df['Visceral Fat'] = df['Visceral Fat'].astype(float)
            df['Body Water'] = df['Body Water'].str.replace('%', '').astype(float)
            df['Muscle Mass'] = df['Muscle Mass'].str.replace('lb', '').astype(float) * 0.453592  # Convert to kg
            df['Bone Mass'] = df['Bone Mass'].str.replace('lb', '').astype(float) * 0.453592  # Convert to kg
            df['BMR'] = df['BMR'].str.replace('kcal', '').astype(float)
            
            # Group by date and take latest measurement
            daily_data = df.groupby('date').last().reset_index()
            
            return daily_data
        except Exception as e:
            print(f"Error loading Starfit data: {e}")
            return pd.DataFrame()
    
    def load_elitehrv_data(self):
        """Load and process EliteHRV data"""
        try:
            df = pd.read_csv(f"{self.data_dir}/polar/elitehrv_03292024.csv")
            
            # Parse dates
            df['date'] = pd.to_datetime(df['Date Time Start']).dt.date
            
            # Group by date and calculate daily averages
            daily_data = df.groupby('date').agg({
                'HRV': 'mean',
                'Morning Readiness': 'mean',
                'HR': 'mean',
                'Rmssd': 'mean',
                'Sdnn': 'mean',
                'LF/HF Ratio': 'mean',
                'Total Power': 'mean'
            }).reset_index()
            
            return daily_data
        except Exception as e:
            print(f"Error loading EliteHRV data: {e}")
            return pd.DataFrame()
    
    def load_dexcom_data(self):
        """Load and process Dexcom CGM data"""
        try:
            df = pd.read_csv(f"{self.data_dir}/dexcom/glucose_readings_oct2025.csv")
            
            # Parse dates
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            
            # Group by date and calculate daily averages
            daily_data = df.groupby('date').agg({
                'glucose_mg_dl': 'mean',
                'time_in_range_pct': 'mean',
                'gmi_percent': 'mean',
                'coefficient_variation': 'mean',
                'mean_glucose_mg_dl': 'mean',
                'sensor_usage_pct': 'mean'
            }).reset_index()
            
            return daily_data
        except Exception as e:
            print(f"Error loading Dexcom data: {e}")
            return pd.DataFrame()
    
    def load_pison_data(self):
        """Load and process Pison neurophysiological data"""
        try:
            df = pd.read_csv(f"{self.data_dir}/pison/emg_readings_oct2025.csv")
            
            # Parse dates
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            
            # Group by date and calculate daily averages
            daily_data = df.groupby('date').agg({
                'readiness_score': 'mean',
                'mental_agility_score': 'mean',
                'focus_score': 'mean',
                'neural_sleep_quality': 'mean',
                'neural_sleep_debt_min': 'mean',
                'sleep_efficiency_pct': 'mean',
                'hrv_ms': 'mean',
                'heart_rate_bpm': 'mean',
                'steps_count': 'sum',
                'calories_burned': 'sum',
                'eda_stress_level': 'mean',
                'skin_temp_celsius': 'mean',
                'circadian_compliance_pct': 'mean'
            }).reset_index()
            
            return daily_data
        except Exception as e:
            print(f"Error loading Pison data: {e}")
            return pd.DataFrame()
    
    def calculate_risk_scores(self, row):
        """Calculate clinical risk scores based on data"""
        risk_scores = {}
        
        # Cardiovascular Risk Score
        hrv = row.get('avg_hrv_ms', 0)
        resting_hr = row.get('avg_resting_hr_bpm', 0)
        recovery = row.get('recovery_score_pct', 0)
        
        if hrv < 30 or resting_hr > 100 or recovery < 40:
            risk_scores['cardiovascular_risk_score'] = 'Abnormality suspected'
        else:
            risk_scores['cardiovascular_risk_score'] = 'No abnormality suspected'
        
        # Neurological Risk Score
        cognitive_readiness = row.get('cognitive_readiness_score', 0)
        focus = row.get('focus_score', 0)
        stress = row.get('stress_level', 0)
        
        if cognitive_readiness < 50 or focus < 50 or stress > 4:
            risk_scores['neurological_risk_score'] = 'Abnormality suspected'
        else:
            risk_scores['neurological_risk_score'] = 'No abnormality suspected'
        
        # Metabolic Risk Score
        tir = row.get('time_in_range_pct', 0)
        gmi = row.get('gmi_percent', 0)
        
        if tir < 60 or gmi > 6.5:
            risk_scores['metabolic_risk_score'] = 'Abnormality suspected'
        else:
            risk_scores['metabolic_risk_score'] = 'No abnormality suspected'
        
        # Skeletal Risk Score (based on body composition trends)
        muscle_mass = row.get('muscle_mass_kg', 0)
        bone_mass = row.get('bone_mass_kg', 0)
        
        if muscle_mass < 50 or bone_mass < 5:
            risk_scores['skeletal_risk_score'] = 'Abnormality suspected'
        else:
            risk_scores['skeletal_risk_score'] = 'No abnormality suspected'
        
        return risk_scores
    
    def calculate_trends(self, df, metric, window=30):
        """Calculate 30-day trends for key metrics"""
        df_sorted = df.sort_values('date')
        trends = []
        
        for i, row in df_sorted.iterrows():
            if i < window - 1:
                trends.append('insufficient_data')
            else:
                recent_data = df_sorted.iloc[i-window+1:i+1][metric].dropna()
                if len(recent_data) < 5:
                    trends.append('insufficient_data')
                else:
                    slope = np.polyfit(range(len(recent_data)), recent_data, 1)[0]
                    if slope > 0.1:
                        trends.append('improving')
                    elif slope < -0.1:
                        trends.append('declining')
                    else:
                        trends.append('stable')
        
        return trends
    
    def harmonize_data(self):
        """Main harmonization function"""
        print("Loading data from all sources...")
        
        # Load all data sources
        whoop_data = self.load_whoop_data()
        starfit_data = self.load_starfit_data()
        elitehrv_data = self.load_elitehrv_data()
        dexcom_data = self.load_dexcom_data()
        pison_data = self.load_pison_data()
        
        print(f"Loaded data: WHOOP({len(whoop_data)}), Starfit({len(starfit_data)}), "
              f"EliteHRV({len(elitehrv_data)}), Dexcom({len(dexcom_data)}), Pison({len(pison_data)})")
        
        # Create date range for all data
        all_dates = set()
        for df in [whoop_data, starfit_data, elitehrv_data, dexcom_data, pison_data]:
            if not df.empty:
                all_dates.update(df['date'].tolist())
        
        date_range = pd.DataFrame({'date': sorted(all_dates)})
        
        # Merge all data sources
        print("Merging data sources...")
        unified_data = date_range.copy()
        
        # Merge each data source
        for name, data in [('whoop', whoop_data), ('starfit', starfit_data), 
                          ('elitehrv', elitehrv_data), ('dexcom', dexcom_data), 
                          ('pison', pison_data)]:
            if not data.empty:
                unified_data = unified_data.merge(data, on='date', how='left', suffixes=('', f'_{name}'))
        
        # Map fields to unified schema
        print("Mapping fields to unified schema...")
        harmonized_data = pd.DataFrame()
        
        # Basic fields
        harmonized_data['date'] = unified_data['date']
        harmonized_data['patient_id'] = 'patient_001'
        
        # Cardiovascular Health
        harmonized_data['avg_resting_hr_bpm'] = unified_data.get('Resting heart rate (bpm)', 
                                                               unified_data.get('heart_rate_bpm', np.nan))
        harmonized_data['avg_hrv_ms'] = unified_data.get('Heart rate variability (ms)', 
                                                        unified_data.get('HRV', 
                                                                       unified_data.get('hrv_ms', np.nan)))
        harmonized_data['cardiac_index'] = unified_data.get('Cardiac Index', np.nan)
        
        # Metabolic Health
        harmonized_data['avg_glucose_mg_dl'] = unified_data.get('glucose_mg_dl', np.nan)
        harmonized_data['time_in_range_pct'] = unified_data.get('time_in_range_pct', np.nan)
        harmonized_data['gmi_percent'] = unified_data.get('gmi_percent', np.nan)
        harmonized_data['glucose_variability_cv'] = unified_data.get('coefficient_variation', np.nan)
        
        # Body Composition
        harmonized_data['weight_kg'] = unified_data.get('Weight', np.nan)
        harmonized_data['bmi'] = unified_data.get('BMI', np.nan)
        harmonized_data['body_fat_pct'] = unified_data.get('Body Fat', np.nan)
        harmonized_data['muscle_mass_kg'] = unified_data.get('Muscle Mass', np.nan)
        harmonized_data['visceral_fat_level'] = unified_data.get('Visceral Fat', np.nan)
        harmonized_data['bone_mass_kg'] = unified_data.get('Bone Mass', np.nan)
        harmonized_data['body_water_pct'] = unified_data.get('Body Water', np.nan)
        
        # Sleep & Recovery
        harmonized_data['sleep_duration_hours'] = unified_data.get('sleep_duration_hours', np.nan)
        harmonized_data['sleep_efficiency_pct'] = unified_data.get('Sleep efficiency %', 
                                                                 unified_data.get('sleep_efficiency_pct', np.nan))
        harmonized_data['sleep_consistency_pct'] = unified_data.get('Sleep consistency %', np.nan)
        harmonized_data['deep_sleep_pct'] = unified_data.get('deep_sleep_pct', np.nan)
        harmonized_data['rem_sleep_pct'] = unified_data.get('rem_sleep_pct', np.nan)
        harmonized_data['sleep_debt_hours'] = unified_data.get('sleep_debt_hours', np.nan)
        harmonized_data['recovery_score_pct'] = unified_data.get('Recovery score %', np.nan)
        
        # Cognitive & Neurological
        harmonized_data['cognitive_readiness_score'] = unified_data.get('readiness_score', np.nan)
        harmonized_data['mental_agility_score'] = unified_data.get('mental_agility_score', np.nan)
        harmonized_data['focus_score'] = unified_data.get('focus_score', np.nan)
        harmonized_data['stress_level'] = unified_data.get('eda_stress_level', np.nan)
        harmonized_data['circadian_compliance_pct'] = unified_data.get('circadian_compliance_pct', np.nan)
        
        # Activity & Fitness
        harmonized_data['daily_strain_score'] = unified_data.get('Day Strain', np.nan)
        harmonized_data['energy_expenditure_kcal'] = unified_data.get('Energy burned (cal)', 
                                                                    unified_data.get('calories_burned', np.nan))
        harmonized_data['steps_count'] = unified_data.get('steps_count', np.nan)
        
        # Vital Signs
        harmonized_data['skin_temperature_celsius'] = unified_data.get('Skin temp (celsius)', 
                                                                     unified_data.get('skin_temp_celsius', np.nan))
        harmonized_data['blood_oxygen_pct'] = unified_data.get('Blood oxygen %', np.nan)
        harmonized_data['respiratory_rate_rpm'] = unified_data.get('Respiratory rate (rpm)', np.nan)
        
        # Calculate risk scores
        print("Calculating clinical risk scores...")
        risk_scores = []
        for _, row in harmonized_data.iterrows():
            risk_scores.append(self.calculate_risk_scores(row))
        
        risk_df = pd.DataFrame(risk_scores)
        harmonized_data = pd.concat([harmonized_data, risk_df], axis=1)
        
        # Calculate trends
        print("Calculating 30-day trends...")
        harmonized_data['weight_trend_30d'] = self.calculate_trends(harmonized_data, 'weight_kg')
        harmonized_data['glucose_trend_30d'] = self.calculate_trends(harmonized_data, 'avg_glucose_mg_dl')
        harmonized_data['hrv_trend_30d'] = self.calculate_trends(harmonized_data, 'avg_hrv_ms')
        harmonized_data['sleep_trend_30d'] = self.calculate_trends(harmonized_data, 'sleep_duration_hours')
        harmonized_data['recovery_trend_30d'] = self.calculate_trends(harmonized_data, 'recovery_score_pct')
        
        # Calculate data quality scores
        print("Calculating data quality scores...")
        data_quality = []
        for _, row in harmonized_data.iterrows():
            quality_score = 0
            total_fields = 0
            
            # Check each data source
            sources = {
                'whoop': ['avg_resting_hr_bpm', 'avg_hrv_ms', 'recovery_score_pct'],
                'starfit': ['weight_kg', 'bmi', 'body_fat_pct'],
                'elitehrv': ['avg_hrv_ms'],
                'dexcom': ['avg_glucose_mg_dl', 'time_in_range_pct'],
                'pison': ['cognitive_readiness_score', 'mental_agility_score']
            }
            
            for source, fields in sources.items():
                source_quality = sum(1 for field in fields if pd.notna(row.get(field, np.nan))) / len(fields)
                quality_score += source_quality
                total_fields += 1
            
            data_quality.append((quality_score / total_fields) * 100 if total_fields > 0 else 0)
        
        harmonized_data['data_quality_score'] = data_quality
        
        # Add data completeness percentages
        harmonized_data['whoop_data_pct'] = harmonized_data[['avg_resting_hr_bpm', 'avg_hrv_ms', 'recovery_score_pct']].notna().mean(axis=1) * 100
        harmonized_data['starfit_data_pct'] = harmonized_data[['weight_kg', 'bmi', 'body_fat_pct']].notna().mean(axis=1) * 100
        harmonized_data['elitehrv_data_pct'] = harmonized_data[['avg_hrv_ms']].notna().mean(axis=1) * 100
        harmonized_data['dexcom_data_pct'] = harmonized_data[['avg_glucose_mg_dl', 'time_in_range_pct']].notna().mean(axis=1) * 100
        harmonized_data['pison_data_pct'] = harmonized_data[['cognitive_readiness_score', 'mental_agility_score']].notna().mean(axis=1) * 100
        
        # Add placeholder fields for clinical notes
        harmonized_data['physician_notes'] = ''
        harmonized_data['patient_reported_symptoms'] = ''
        harmonized_data['medication_changes'] = ''
        harmonized_data['life_events'] = ''
        
        # Add derived clinical indicators
        harmonized_data['inflammation_markers'] = 'low'  # Placeholder
        harmonized_data['oxidative_stress_level'] = 'moderate'  # Placeholder
        harmonized_data['autonomic_balance_score'] = 'balanced'  # Placeholder
        harmonized_data['metabolic_age'] = 22  # Placeholder
        
        # Add missing fields with NaN
        for field in self.unified_schema:
            if field not in harmonized_data.columns:
                harmonized_data[field] = np.nan
        
        # Reorder columns to match schema
        harmonized_data = harmonized_data[self.unified_schema]
        
        return harmonized_data
    
    def export_harmonized_data(self, output_file="harmonized_health_data.csv"):
        """Export harmonized data to CSV"""
        harmonized_data = self.harmonize_data()
        
        print(f"Exporting harmonized data to {output_file}...")
        harmonized_data.to_csv(output_file, index=False)
        
        print(f"Successfully exported {len(harmonized_data)} records")
        print(f"Data quality score range: {harmonized_data['data_quality_score'].min():.1f}% - {harmonized_data['data_quality_score'].max():.1f}%")
        
        return harmonized_data

def main():
    """Main execution function"""
    print("Starting Health Data Harmonization...")
    
    harmonizer = HealthDataHarmonizer()
    harmonized_data = harmonizer.export_harmonized_data()
    
    print("\nSample of harmonized data:")
    print(harmonized_data.head())
    
    print("\nData summary:")
    print(f"Total records: {len(harmonized_data)}")
    print(f"Date range: {harmonized_data['date'].min()} to {harmonized_data['date'].max()}")
    print(f"Average data quality: {harmonized_data['data_quality_score'].mean():.1f}%")

if __name__ == "__main__":
    main()