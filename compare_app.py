"""
AI & Cloud Energy Consumption: Country Comparison Tool

A Streamlit application for comparing energy consumption and carbon footprint
of AI and cloud computing tasks between two different electrical grids.
"""

from typing import Dict, List, Tuple, Any
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="AI Energy: Country Comparison",
    page_icon="🌍",
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

def calculate_impact(user_inputs: Dict[str, Dict[str, Any]], carbon_intensity: int) -> Tuple[float, float]:
    """
    Calculate total energy consumption and carbon impact.
    
    Args:
        user_inputs: Dictionary containing user input data with energy consumption
        carbon_intensity: Grid carbon intensity in grams CO2 per kWh
        
    Returns:
        Tuple of (total_energy_wh, co2_kg) where:
        - total_energy_wh: Total energy consumption in watt-hours
        - co2_kg: Total CO2 emissions in kilograms
    """
    total_energy: float = sum(data["total_energy"] for data in user_inputs.values())
    co2_grams: float = (total_energy / 1000) * carbon_intensity
    co2_kg: float = co2_grams / 1000
    return total_energy, co2_kg

def main() -> None:
    """
    Main function that runs the country comparison Streamlit application.
    
    Creates an interactive web interface for comparing energy consumption
    and carbon footprint of AI and cloud computing tasks between two
    different electrical grids.
    """
    st.title("🌍 AI & Cloud Energy: Country Comparison")
    st.markdown("Compare the carbon footprint of your digital activities across different countries")
    
    # Introduction and instructions
    with st.expander("ℹ️ How to Use This Comparison Tool", expanded=False):
        st.markdown("""
        **Welcome to the Country Comparison Tool!**
        
        This tool demonstrates how the same digital activities can have dramatically different environmental impacts depending on where they're performed, based on each country's electricity grid composition.
        
        **How it works:**
        1. **Select two countries** - Choose any two locations to compare their grid carbon intensities
        2. **Enter your activities** - Input the same quantities you would use in both countries
        3. **Compare the impact** - See side-by-side charts showing how much more (or less) CO₂ is produced in each location
        
        **Key insights:**
        - **Grid composition matters** - Countries with more renewable energy (like Iceland with geothermal) produce far less CO₂
        - **Same task, different impact** - Generating an AI image in Iceland vs Texas can differ by over 20x in carbon emissions
        - **Location awareness** - Understanding your grid's carbon intensity can help you make more environmentally conscious choices
        
        **The numbers:**
        - Iceland: 18 g CO₂/kWh (geothermal & hydro)
        - France: 79 g CO₂/kWh (nuclear & renewables)
        - UK: 233 g CO₂/kWh (mixed grid)
        - USA/Texas: 400 g CO₂/kWh (fossil fuel heavy)
        """)
    

    # Country selection
    col_select1, col_select2 = st.columns(2)
    
    with col_select1:
        st.subheader("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Country A")
        country_a = st.selectbox(
            "Select first country:",
            options=list(grid_carbon_intensity.keys()),
            index=0,
            key="country_a_select"
        )
        intensity_a = grid_carbon_intensity[country_a]
        st.info(f"Grid: {intensity_a} g CO₂/kWh")
    
    with col_select2:
        st.subheader("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Country B")
        country_b = st.selectbox(
            "Select second country:",
            options=list(grid_carbon_intensity.keys()),
            index=3,
            key="country_b_select"
        )
        intensity_b = grid_carbon_intensity[country_b]
        st.info(f"Grid: {intensity_b} g CO₂/kWh")
    
    st.markdown("---")
    
    # Input section
    st.header("🔧 Configure Your Digital Activities")
    
    # Store user inputs
    user_inputs: Dict[str, Dict[str, Any]] = {}
    
    # Create input columns
    col_ai, col_cloud = st.columns(2)
    
    with col_ai:
        st.subheader("🤖 AI Tasks")
        for task, base_energy in energy_data["AI Tasks"].items():
            quantity = st.number_input(
                f"{task}",
                min_value=0,
                value=0,
                step=1,
                key=f"ai_{task}",
                help=f"{base_energy} Wh per task"
            )
            if quantity > 0:
                task_energy = quantity * base_energy
                user_inputs[task] = {
                    "quantity": quantity, 
                    "unit_energy": base_energy, 
                    "total_energy": task_energy,
                    "category": "AI"
                }
    
    with col_cloud:
        st.subheader("☁️ Data & Cloud Tasks")
        for task, base_energy in energy_data["Data & Cloud Tasks"].items():
            quantity = st.number_input(
                f"{task}",
                min_value=0,
                value=0,
                step=1,
                key=f"data_{task}",
                help=f"{base_energy} Wh per task"
            )
            if quantity > 0:
                task_energy = quantity * base_energy
                user_inputs[task] = {
                    "quantity": quantity, 
                    "unit_energy": base_energy, 
                    "total_energy": task_energy,
                    "category": "Cloud"
                }
    
    if user_inputs:
        st.markdown("---")
        
        # Calculate impacts for both countries
        total_energy_a, co2_kg_a = calculate_impact(user_inputs, intensity_a)
        total_energy_b, co2_kg_b = calculate_impact(user_inputs, intensity_b)
        
        # Comparison overview
        st.header("⚖️ Impact Comparison")
        
        col_comp1, col_comp2, col_comp3 = st.columns(3)
        
        with col_comp1:
            st.metric(
                "Energy Consumption", 
                f"{total_energy_a:,.1f} Wh",
                help="Same for both countries"
            )
        
        with col_comp2:
            st.metric(
                f"CO₂ in {country_a}", 
                f"{co2_kg_a:.3f} kg",
                f"{(co2_kg_a * 1000):.1f} g"
            )
        
        with col_comp3:
            st.metric(
                f"CO₂ in {country_b}", 
                f"{co2_kg_b:.3f} kg",
                f"{(co2_kg_b * 1000):.1f} g"
            )
        
        # Impact difference
        if co2_kg_a != co2_kg_b:
            difference = abs(co2_kg_a - co2_kg_b)
            ratio = max(co2_kg_a, co2_kg_b) / min(co2_kg_a, co2_kg_b)
            cleaner_country = country_a if co2_kg_a < co2_kg_b else country_b
            
            st.success(f"💡 **{cleaner_country}** produces {difference:.3f} kg ({difference*1000:.0f} g) less CO₂ - that's {ratio:.1f}x cleaner!")
        
        # Side-by-side comparison charts with synchronized scales
        col_chart1, col_chart2 = st.columns(2)
        
        # Calculate data for both countries first to determine max scale
        chart_data_a = []
        chart_data_b = []
        max_co2 = 0
        
        for task, data in user_inputs.items():
            co2_task_a = (data["total_energy"] / 1000) * intensity_a
            co2_task_b = (data["total_energy"] / 1000) * intensity_b
            max_co2 = max(max_co2, co2_task_a, co2_task_b)
            
            chart_data_a.append({
                "Task": task[:25] + "..." if len(task) > 25 else task,
                "CO₂ (g)": co2_task_a,
                "Energy (Wh)": data["total_energy"],
                "Category": data["category"]
            })
            
            chart_data_b.append({
                "Task": task[:25] + "..." if len(task) > 25 else task,
                "CO₂ (g)": co2_task_b,
                "Energy (Wh)": data["total_energy"],
                "Category": data["category"]
            })
        
        # Enhanced color scheme for better differentiation
        color_map = {
            "AI": "#e74c3c",      # Red for AI tasks
            "Cloud": "#3498db"    # Blue for Cloud tasks
        }
        
        # Country A breakdown
        with col_chart1:
            st.subheader(f"📊 {country_a} Breakdown")
            
            df_a = pd.DataFrame(chart_data_a)
            fig_a = px.bar(
                df_a,
                x="CO₂ (g)",
                y="Task",
                orientation='h',
                title=f"CO₂ Impact in {country_a}",
                color="Category",
                color_discrete_map=color_map
            )
            # Set consistent x-axis range
            fig_a.update_layout(
                height=400, 
                showlegend=True,
                xaxis=dict(range=[0, max_co2 * 1.05]),  # Add 5% padding
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_a, use_container_width=True)
        
        # Country B breakdown
        with col_chart2:
            st.subheader(f"📊 {country_b} Breakdown")
            
            df_b = pd.DataFrame(chart_data_b)
            fig_b = px.bar(
                df_b,
                x="CO₂ (g)",
                y="Task",
                orientation='h',
                title=f"CO₂ Impact in {country_b}",
                color="Category",
                color_discrete_map=color_map
            )
            # Set consistent x-axis range
            fig_b.update_layout(
                height=400,
                showlegend=True,
                xaxis=dict(range=[0, max_co2 * 1.05]),  # Same scale as country A
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_b, use_container_width=True)
        
        # Direct comparison chart
        st.subheader("🔄 Direct Comparison")
        
        comparison_data = []
        for task, data in user_inputs.items():
            co2_a = (data["total_energy"] / 1000) * intensity_a
            co2_b = (data["total_energy"] / 1000) * intensity_b
            
            comparison_data.extend([
                {
                    "Task": task[:30] + "..." if len(task) > 30 else task,
                    "Country": country_a,
                    "CO₂ (g)": co2_a,
                    "Category": data["category"]
                },
                {
                    "Task": task[:30] + "..." if len(task) > 30 else task,
                    "Country": country_b,
                    "CO₂ (g)": co2_b,
                    "Category": data["category"]
                }
            ])
        
        comparison_df = pd.DataFrame(comparison_data)
        
        fig_comparison = px.bar(
            comparison_df,
            x="Task",
            y="CO₂ (g)",
            color="Country",
            barmode="group",
            title="CO₂ Impact Comparison by Task",
            color_discrete_sequence=["#3498db", "#e74c3c"]
        )
        fig_comparison.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Environmental equivalents comparison
        st.subheader("🌱 Environmental Impact Equivalents")
        
        col_env1, col_env2 = st.columns(2)
        
        with col_env1:
            st.markdown(f"**{country_a}**")
            trees_days_a = co2_kg_a / (22 / 365)
            car_seconds_a = co2_kg_a / (4.6 * 1000 / 365 / 24 / 3600)
            
            st.metric("Tree Days to Offset", f"{trees_days_a:.2f}")
            if car_seconds_a < 60:
                st.metric("Car Driving Equivalent", f"{car_seconds_a:.0f} sec")
            elif car_seconds_a < 3600:
                st.metric("Car Driving Equivalent", f"{car_seconds_a/60:.1f} min")
            else:
                st.metric("Car Driving Equivalent", f"{car_seconds_a/3600:.2f} hrs")
        
        with col_env2:
            st.markdown(f"**{country_b}**")
            trees_days_b = co2_kg_b / (22 / 365)
            car_seconds_b = co2_kg_b / (4.6 * 1000 / 365 / 24 / 3600)
            
            st.metric("Tree Days to Offset", f"{trees_days_b:.2f}")
            if car_seconds_b < 60:
                st.metric("Car Driving Equivalent", f"{car_seconds_b:.0f} sec")
            elif car_seconds_b < 3600:
                st.metric("Car Driving Equivalent", f"{car_seconds_b/60:.1f} min")
            else:
                st.metric("Car Driving Equivalent", f"{car_seconds_b/3600:.2f} hrs")
        
        # Summary table
        st.subheader("📋 Detailed Comparison Table")
        
        summary_data = []
        for task, data in user_inputs.items():
            co2_a = (data["total_energy"] / 1000) * intensity_a
            co2_b = (data["total_energy"] / 1000) * intensity_b
            difference = abs(co2_a - co2_b)
            
            summary_data.append({
                "Task": task,
                "Quantity": data["quantity"],
                "Energy (Wh)": data["total_energy"],
                f"{country_a} CO₂ (g)": round(co2_a, 2),
                f"{country_b} CO₂ (g)": round(co2_b, 2),
                "Difference (g)": round(difference, 2)
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True)
    
    else:
        st.info("👆 Enter some quantities above to see the comparison between countries!")

if __name__ == "__main__":
    main()