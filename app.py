"""
AI & Cloud Energy Consumption Calculator

A Streamlit application for calculating energy consumption and carbon footprint
of various AI and cloud computing tasks across different electrical grids.
"""

from typing import Dict, List, Tuple, Any
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="AI & Cloud Energy Calculator",
    page_icon="⚡",
    layout="wide"
)

# Grid carbon intensity data (grams CO2 per kWh)
grid_carbon_intensity: Dict[str, int] = {
    "UK": 233,  # 2023 average
    "France": 79,  # 2023 average (high nuclear)
    "Iceland": 18,  # 2023 average (geothermal/hydro)
    "USA/Texas": 400,  # 2023 average (high fossil fuel mix)
}

# Energy consumption data (watt-hours per task)
energy_data: Dict[str, Dict[str, float]] = {
    "AI Tasks": {
        "Generate a paragraph of AI text": 7,
        "Generate 100 lines of code using an AI tool": 0.5,
        "Generate a 1024x1024 pixel AI image": 2,
        "Generate a 30-second AI music track": 100,
        "Transcribe 1 hour of audio with AI": 10,
        "Generate a 3-second AI video from text": 500,
        "Generate a 3-second AI video from image": 650,
    },
    "Data & Cloud Tasks": {
        "Do a Google search without AI summary": 0.3,
        "Charging a smartphone": 20,
        "Storing 1000 photographs in the cloud for 1 month": 8,
        "Stream music for 1 hour": 75,
        "Watching 1-hour of content on Netflix": 200,
        "Video-calling for 1 hour with 10 people": 2000,
    }
}

def main() -> None:
    """
    Main function that runs the Streamlit application.
    
    Creates an interactive web interface for calculating energy consumption
    and carbon footprint of AI and cloud computing tasks across different
    electrical grids.
    """
    st.title("⚡ AI & Cloud Energy Consumption Calculator")
    st.markdown("Calculate the energy footprint of your digital activities")
    
    # Introduction and instructions
    with st.expander("ℹ️ How to Use This Calculator", expanded=False):
        st.markdown("""
        **Welcome to the AI & Cloud Energy Calculator!**
        
        This tool helps you understand the environmental impact of your digital activities by calculating their energy consumption and carbon footprint.
        
        **How it works:**
        1. **Choose your location** - Different countries have different carbon intensities based on their energy mix (renewable vs fossil fuels)
        2. **Enter your activities** - Input how many times you perform various AI and cloud computing tasks
        3. **View your impact** - See your total energy consumption, carbon footprint, and helpful comparisons
        
        **Understanding the results:**
        - **Energy consumption** is measured in watt-hours (Wh) - the same unit used for your household electricity
        - **Carbon footprint** varies dramatically by location - the same task in Iceland produces far less CO₂ than in Texas
        - **Equivalents** help put your impact in perspective (smartphone charges, Netflix hours, etc.)
        
        The data is based on recent research into the energy consumption of AI models and cloud computing infrastructure.
        """)
    

    # Create two columns for input and results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🔧 Configure Your Usage")
        
        # Location selection
        st.subheader("🌍 Select Your Location")
        selected_location = st.selectbox(
            "Choose your grid location:",
            options=list(grid_carbon_intensity.keys()),
            help="Different locations have different carbon intensities based on their energy mix",
            key="location_select"
        )
        
        carbon_intensity = grid_carbon_intensity[selected_location]
        st.info(f"Grid carbon intensity: {carbon_intensity} g CO₂/kWh")
        
        # Store user inputs
        user_inputs: Dict[str, Dict[str, Any]] = {}
        total_energy: float = 0
        
        # AI Tasks section
        st.subheader("🤖 AI Tasks")
        for task, base_energy in energy_data["AI Tasks"].items():
            quantity = st.number_input(
                f"{task} ({base_energy} Wh each)",
                min_value=0,
                value=0,
                step=1,
                key=f"ai_{task}"
            )
            if quantity > 0:
                task_energy = quantity * base_energy
                user_inputs[task] = {"quantity": quantity, "unit_energy": base_energy, "total_energy": task_energy}
                total_energy += task_energy
        
        # Data & Cloud Tasks section
        st.subheader("☁️ Data & Cloud Tasks")
        for task, base_energy in energy_data["Data & Cloud Tasks"].items():
            quantity = st.number_input(
                f"{task} ({base_energy} Wh each)",
                min_value=0,
                value=0,
                step=1,
                key=f"data_{task}"
            )
            if quantity > 0:
                task_energy = quantity * base_energy
                user_inputs[task] = {"quantity": quantity, "unit_energy": base_energy, "total_energy": task_energy}
                total_energy += task_energy
    
    with col2:
        st.header("📊 Energy Consumption Results")
        
        if total_energy > 0:
            # Display total energy
            st.metric("Total Energy Consumption", f"{total_energy:,.1f} Wh", f"{total_energy/1000:.2f} kWh")
            
            # Energy equivalents
            st.subheader("🔋 Energy Equivalents")
            smartphone_charges = total_energy / 20
            netflix_hours = total_energy / 200
            
            col_eq1, col_eq2 = st.columns(2)
            with col_eq1:
                st.metric("Smartphone Charges", f"{smartphone_charges:.1f}")
            with col_eq2:
                st.metric("Hours of Netflix", f"{netflix_hours:.1f}")
            
            # Create breakdown chart
            if user_inputs:
                st.subheader("📈 Energy Breakdown")
                
                # Prepare data for chart
                chart_data = []
                for task, data in user_inputs.items():
                    chart_data.append({
                        "Task": task[:30] + "..." if len(task) > 30 else task,
                        "Energy (Wh)": data["total_energy"],
                        "Quantity": data["quantity"]
                    })
                
                df = pd.DataFrame(chart_data)
                
                # Create bar chart
                fig = px.bar(
                    df, 
                    x="Energy (Wh)", 
                    y="Task",
                    orientation='h',
                    title="Energy Consumption by Task",
                    color="Energy (Wh)",
                    color_continuous_scale="Reds"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed breakdown table
                st.subheader("📋 Detailed Breakdown")
                display_df = pd.DataFrame([
                    {
                        "Task": task,
                        "Quantity": data["quantity"],
                        "Unit Energy (Wh)": data["unit_energy"],
                        "Total Energy (Wh)": data["total_energy"]
                    }
                    for task, data in user_inputs.items()
                ])
                st.dataframe(display_df, use_container_width=True)
        
        else:
            st.info("👆 Enter some quantities above to see your energy consumption!")
    
    # Environmental impact section
    if total_energy > 0:
        st.header(f"🌍 Environmental Impact ({selected_location})")
        
        # CO2 equivalent using location-specific grid carbon intensity
        co2_grams = (total_energy / 1000) * carbon_intensity
        co2_kg = co2_grams / 1000
        
        col_env1, col_env2, col_env3 = st.columns(3)
        with col_env1:
            st.metric("CO₂ Equivalent", f"{co2_kg:.3f} kg", f"{co2_grams:.1f} g")
        with col_env2:
            # Tree equivalent (1 tree absorbs ~22 kg CO2 per year)
            trees_days = co2_kg / (22 / 365)
            st.metric("Tree Days to Offset", f"{trees_days:.2f}")
        with col_env3:
            # Car equivalent (average car emits 4.6 metric tons CO2 per year = 12.6 kg/day)
            car_seconds = (co2_kg / (4.6 * 1000 / 365 / 24 / 3600))
            if car_seconds < 60:
                st.metric("Car Driving Equivalent", f"{car_seconds:.0f} seconds")
            elif car_seconds < 3600:
                st.metric("Car Driving Equivalent", f"{car_seconds/60:.1f} minutes")
            else:
                st.metric("Car Driving Equivalent", f"{car_seconds/3600:.2f} hours")
        
        # Comparison across locations
        st.subheader("🗺️ Location Comparison")
        comparison_data = []
        for location, intensity in grid_carbon_intensity.items():
            location_co2 = (total_energy / 1000) * intensity / 1000  # kg
            comparison_data.append({
                "Location": location,
                "Grid Intensity (g CO₂/kWh)": intensity,
                "Your CO₂ Impact (kg)": location_co2,
                "Relative to " + selected_location: location_co2 / co2_kg
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Create comparison chart
        fig_comparison = px.bar(
            comparison_df,
            x="Location",
            y="Your CO₂ Impact (kg)",
            title="CO₂ Impact by Grid Location",
            color="Grid Intensity (g CO₂/kWh)",
            color_continuous_scale="RdYlGn_r"
        )
        fig_comparison.update_layout(height=300)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Show comparison table
        st.dataframe(comparison_df.round(3), use_container_width=True)

if __name__ == "__main__":
    main()