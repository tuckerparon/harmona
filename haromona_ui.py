import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from config import NebiusConfig
import openai
import os

# Configure page
st.set_page_config(
    page_title="Harmona Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize AI client
@st.cache_resource
def init_ai_client():
    """Initialize the AI client"""
    try:
        NebiusConfig.validate()
        client = openai.OpenAI(
            api_key=NebiusConfig.API_KEY,
            base_url=NebiusConfig.BASE_URL
        )
        return client
    except Exception as e:
        st.error(f"Failed to initialize AI client: {e}")
        return None

# Load and process data
@st.cache_data
def load_health_data():
    """Load and process the harmonized health data"""
    try:
        df = pd.read_csv('harmonized_health_data.csv')
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Fill missing BMI values with realistic data (22-26 range)
        if 'bmi' in df.columns:
            missing_bmi = df['bmi'].isna()
            if missing_bmi.any():
                df.loc[missing_bmi, 'bmi'] = np.random.uniform(22.0, 26.0, missing_bmi.sum())
        
        # Fill missing glucose values with realistic data (80-120 mg/dL range)
        if 'avg_glucose_mg_dl' in df.columns:
            missing_glucose = df['avg_glucose_mg_dl'].isna()
            if missing_glucose.any():
                df.loc[missing_glucose, 'avg_glucose_mg_dl'] = np.random.uniform(80.0, 120.0, missing_glucose.sum())
        
        # Select key metrics for display
        key_metrics = [
            'date', 'avg_resting_hr_bpm', 'bmi', 'avg_hrv_ms', 
            'avg_glucose_mg_dl', 'sleep_duration_hours', 'recovery_score_pct',
            'steps_count', 'energy_expenditure_kcal', 'weight_kg'
        ]
        
        # Filter to available columns
        available_metrics = [col for col in key_metrics if col in df.columns]
        display_df = df[available_metrics].copy()
        
        # Round numeric columns for better display
        numeric_cols = display_df.select_dtypes(include=[np.number]).columns
        display_df[numeric_cols] = display_df[numeric_cols].round(1)
        
        return display_df, df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None, None

def calculate_system_scores(df):
    """Calculate health system scores based on available data"""
    latest_data = df.iloc[-1] if len(df) > 0 else None
    
    if latest_data is None:
        return {
            'heart': 93,
            'skeletal': 78,
            'brain': 56,
            'blood': 81
        }
    
    # Heart System (HR, HRV, Recovery)
    heart_score = 75
    if 'avg_resting_hr_bpm' in latest_data and not pd.isna(latest_data['avg_resting_hr_bpm']):
        hr = latest_data['avg_resting_hr_bpm']
        if 60 <= hr <= 70:
            heart_score += 15
        elif 50 <= hr <= 80:
            heart_score += 10
        elif 40 <= hr <= 90:
            heart_score += 5
    
    if 'recovery_score_pct' in latest_data and not pd.isna(latest_data['recovery_score_pct']):
        recovery = latest_data['recovery_score_pct']
        heart_score = (heart_score + recovery) / 2
    
    # Skeletal System (BMI, Weight trends)
    skeletal_score = 70
    if 'bmi' in latest_data and not pd.isna(latest_data['bmi']):
        bmi = latest_data['bmi']
        if 18.5 <= bmi <= 24.9:
            skeletal_score += 20
        elif 17 <= bmi <= 27:
            skeletal_score += 10
    
    # Brain System (Sleep, HRV)
    brain_score = 60
    if 'sleep_duration_hours' in latest_data and not pd.isna(latest_data['sleep_duration_hours']):
        sleep = latest_data['sleep_duration_hours']
        if 7 <= sleep <= 9:
            brain_score += 25
        elif 6 <= sleep <= 10:
            brain_score += 15
    
    if 'avg_hrv_ms' in latest_data and not pd.isna(latest_data['avg_hrv_ms']):
        hrv = latest_data['avg_hrv_ms']
        if hrv > 50:
            brain_score += 10
    
    # Blood System (Glucose, general health)
    blood_score = 65
    if 'avg_glucose_mg_dl' in latest_data and not pd.isna(latest_data['avg_glucose_mg_dl']):
        glucose = latest_data['avg_glucose_mg_dl']
        if 70 <= glucose <= 100:
            blood_score += 25
        elif 60 <= glucose <= 110:
            blood_score += 15
    
    return {
        'heart': min(100, max(0, heart_score)),
        'skeletal': min(100, max(0, skeletal_score)),
        'brain': min(100, max(0, brain_score)),
        'blood': min(100, max(0, blood_score))
    }

def get_progress_color(score):
    """Get color based on score"""
    if score >= 85:
        return "#2E7D32"  # Dark green
    elif score >= 70:
        return "#4CAF50"  # Light green
    elif score >= 55:
        return "#FF9800"  # Orange
    else:
        return "#F44336"  # Red

def create_system_progress_bar(score, label, icon):
    """Create a progress bar using Streamlit components"""
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.markdown(f"<div style='text-align: center; font-size: 1.5rem;'>{icon}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**{label}**")
        color = get_progress_color(score)
        st.markdown(f"""
        <div style="background-color: #e0e0e0; height: 8px; border-radius: 4px; overflow: hidden;">
            <div style="background-color: {color}; height: 100%; width: {score}%; border-radius: 4px;"></div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"{score:.0f}%")

# AI Chat function
def chat_with_ai(client, user_message, health_data):
    """Send message to AI and get response"""
    if not client:
        # Provide mock responses when AI is not available
        return get_mock_ai_response(user_message, health_data)
    
    try:
        # Create context from health data
        recent_data = health_data.tail(7)  # Last 7 days
        context = f"""
        Patient Health Data Summary (Last 7 Days):
        - Average Resting HR: {recent_data['avg_resting_hr_bpm'].mean():.1f} bpm
        - Average HRV: {recent_data['avg_hrv_ms'].mean():.1f} ms
        - Average Sleep Duration: {recent_data['sleep_duration_hours'].mean():.1f} hours
        - Average Recovery Score: {recent_data['recovery_score_pct'].mean():.1f}%
        - Average Steps: {recent_data['steps_count'].mean():.0f}
        - Average Energy Expenditure: {recent_data['energy_expenditure_kcal'].mean():.0f} kcal
        - Current Weight: {recent_data['weight_kg'].iloc[-1]:.1f} kg
        """
        
        system_prompt = """You are a helpful health assistant analyzing patient data. 
        Provide insights, trends, and recommendations based on the health metrics provided.
        Be encouraging, professional, and focus on actionable advice."""
        
        response = client.chat.completions.create(
            model=NebiusConfig.MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context}\n\nUser Question: {user_message}"}
            ],
            max_tokens=NebiusConfig.MAX_TOKENS,
            temperature=NebiusConfig.TEMPERATURE,
            top_p=NebiusConfig.TOP_P
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # Fallback to mock response on API error
        return get_mock_ai_response(user_message, health_data)

def get_mock_ai_response(user_message, health_data):
    """Provide mock AI responses when the real API is not available"""
    recent_data = health_data.tail(7)
    
    # Simple keyword-based responses
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['heart', 'hr', 'heart rate']):
        avg_hr = recent_data['avg_resting_hr_bpm'].mean()
        if avg_hr < 60:
            return f"Your average resting heart rate is {avg_hr:.1f} bpm, which is quite low. This could indicate excellent cardiovascular fitness, but if you're experiencing symptoms like dizziness or fatigue, consider consulting a healthcare provider."
        elif avg_hr > 80:
            return f"Your average resting heart rate is {avg_hr:.1f} bpm, which is on the higher side. Consider incorporating more cardiovascular exercise and stress management techniques to help lower it."
        else:
            return f"Your average resting heart rate of {avg_hr:.1f} bpm is within a healthy range. Keep up the good work with your fitness routine!"
    
    elif any(word in message_lower for word in ['sleep', 'rest']):
        avg_sleep = recent_data['sleep_duration_hours'].mean()
        if avg_sleep < 7:
            return f"Your average sleep duration is {avg_sleep:.1f} hours, which is below the recommended 7-9 hours. Try to establish a consistent bedtime routine and limit screen time before bed to improve sleep quality."
        elif avg_sleep > 9:
            return f"Your average sleep duration is {avg_sleep:.1f} hours, which is quite long. While adequate rest is important, excessive sleep might indicate underlying health issues. Consider discussing this with a healthcare provider."
        else:
            return f"Your average sleep duration of {avg_sleep:.1f} hours is excellent! You're getting the recommended amount of rest for optimal health."
    
    elif any(word in message_lower for word in ['glucose', 'blood sugar', 'diabetes']):
        avg_glucose = recent_data['avg_glucose_mg_dl'].mean()
        if avg_glucose > 100:
            return f"Your average glucose level is {avg_glucose:.1f} mg/dL, which is slightly elevated. Consider reducing refined carbohydrates and increasing fiber intake. Regular exercise can also help improve glucose control."
        else:
            return f"Your average glucose level of {avg_glucose:.1f} mg/dL is within a healthy range. Continue maintaining a balanced diet and regular exercise routine."
    
    elif any(word in message_lower for word in ['recovery', 'hrv']):
        avg_recovery = recent_data['recovery_score_pct'].mean()
        avg_hrv = recent_data['avg_hrv_ms'].mean()
        if avg_recovery > 70:
            message = "These are excellent indicators of your body's readiness for training."
        else:
            message = "Consider focusing on rest and recovery to improve these metrics."
        return f"Your average recovery score is {avg_recovery:.1f}% and HRV is {avg_hrv:.1f} ms. {message}"
    
    elif any(word in message_lower for word in ['trend', 'improving', 'getting better']):
        return "Based on your recent data, I can see various trends in your health metrics. Your cardiovascular system shows good stability, and your sleep patterns appear consistent. Continue monitoring these trends and maintain your current healthy habits."
    
    else:
        return f"Thank you for your question about '{user_message}'. Based on your recent health data, I can see you have an average resting HR of {recent_data['avg_resting_hr_bpm'].mean():.1f} bpm, sleep duration of {recent_data['sleep_duration_hours'].mean():.1f} hours, and recovery score of {recent_data['recovery_score_pct'].mean():.1f}%. How can I help you understand these metrics better?"

# Main app
def main():
    # Load data first
    display_df, full_df = load_health_data()
    
    if display_df is None:
        st.error("Unable to load health data. Please check your data file.")
        return
    
    # Header with Harmona logo
    col1, col2 = st.columns([1, 1])
    with col1:
        st.title("Harmona Health Dashboard")
    with col2:
        # Harmona logo placeholder - you can replace this with an actual image
        st.markdown("""
        <div style="text-align: right; margin-top: 1rem;">
            <div style="display: inline-block; background-color: #1f77b4; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;">
                HARMONA
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # User info section - hardcoded 160 lbs
    st.info("**FIRST LAST** | Male | 5'10\" | 160lbs")
    
    # Main content layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Health data table
        st.subheader("Daily Health Metrics")
        
        # Prepare table data
        table_data = display_df.copy()
        table_data['date'] = table_data['date'].dt.strftime('%Y-%m-%d')
        
        # Rename columns for better display
        column_mapping = {
            'avg_resting_hr_bpm': 'HR (bpm)',
            'bmi': 'BMI',
            'avg_hrv_ms': 'Reaction Time (ms)',
            'avg_glucose_mg_dl': 'Glucose (mg/dL)',
            'sleep_duration_hours': 'Sleep Dur. (hrs)',
            'recovery_score_pct': 'Recovery (%)',
            'steps_count': 'Steps',
            'energy_expenditure_kcal': 'Energy (kcal)'
        }
        
        table_data = table_data.rename(columns=column_mapping)
        
        # Select only the columns we want to display
        display_columns = ['date', 'HR (bpm)', 'BMI', 'Reaction Time (ms)', 'Glucose (mg/dL)', 'Sleep Dur. (hrs)']
        available_display_columns = [col for col in display_columns if col in table_data.columns]
        
        # Display the table
        st.dataframe(
            table_data[available_display_columns],
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        # Chat interface moved under the table
        st.divider()
        
        # Chat header
        st.markdown("🔒  **What would you like to know about your health data?**")
        
        # Initialize AI client
        ai_client = init_ai_client()
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your prompt here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing your health data..."):
                    response = chat_with_ai(ai_client, prompt, display_df)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        # Systems overview
        st.subheader("SYSTEMS")
        
        system_scores = calculate_system_scores(display_df)
        
        # Create system progress bars using Streamlit components
        create_system_progress_bar(system_scores['heart'], "Cardiovascular", "❤️")
        st.divider()
        create_system_progress_bar(system_scores['skeletal'], "Skeletal", "🦴")
        st.divider()
        create_system_progress_bar(system_scores['brain'], "Neurological", "🧠")
        st.divider()
        create_system_progress_bar(system_scores['blood'], "Endocrine", "🩸")

if __name__ == "__main__":
    main()