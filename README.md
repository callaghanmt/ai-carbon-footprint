# ⚡ AI & Cloud Energy Consumption Calculator

An interactive Streamlit app that calculates the energy footprint and carbon impact of various AI and cloud computing tasks across different grid locations.

## Applications Overview

This project includes two complementary Streamlit applications for analysing the energy consumption and carbon footprint of digital activities:

### 🔋 Single Country Calculator (`app.py`)
**Purpose**: Analyse your digital carbon footprint from one location's perspective

**Key Features**:
- **Location Selection**: Choose from UK, France, Iceland, or USA/Texas electrical grids
- **Task Library**: Input quantities for 10 different AI and cloud computing tasks
- **Real-time Calculations**: Instant energy consumption (Wh/kWh) and CO₂ impact calculations
- **Energy Equivalents**: Compare to familiar references (smartphone charges, Netflix hours)
- **Visual Breakdown**: Interactive charts showing energy consumption by task
- **Environmental Impact**: Tree days to offset, car driving time equivalents
- **Detailed Tables**: Complete breakdown of quantities, unit energy, and totals

**Best For**: 
- Personal carbon footprint awareness
- Understanding your location's grid impact
- Educational purposes about digital energy consumption
- Seeing "what-if" scenarios across different grids

### 🌍 Country Comparison Tool (`compare_app.py`)
**Purpose**: Direct side-by-side comparison of digital activities between two countries

**Key Features**:
- **Dual Country Selection**: Pick any two countries for direct comparison
- **Synchronised Input**: Enter activities once, see impact in both locations
- **Impact Difference Analysis**: Automatic calculation of CO₂ differences and ratios
- **Smart Insights**: Shows which country is cleaner and by how much (e.g., "Iceland is 22x cleaner")
- **Side-by-Side Visualizations**: Parallel breakdown charts for each country
- **Direct Comparison Charts**: Grouped bar charts showing task-by-task differences
- **Environmental Equivalents**: Tree days and car time for both countries
- **Comprehensive Summary Table**: Complete comparison with differences highlighted

**Best For**:
- Data center location decisions
- Policy analysis and research
- Educational demonstrations of grid impact
- Business sustainability planning
- Understanding global digital inequality

## Grid Carbon Intensities

Both applications use real 2023 average grid carbon intensities:

- 🇮🇸 **Iceland**: 18 g CO₂/kWh - Clean geothermal/hydro power
- 🇫🇷 **France**: 79 g CO₂/kWh - Nuclear-heavy grid with renewables
- 🇬🇧 **UK**: 233 g CO₂/kWh - Mixed renewable/fossil fuel grid
- 🇺🇸 **USA/Texas**: 400 g CO₂/kWh - Fossil fuel heavy grid

## Energy Data Coverage

Both applications include energy consumption data for:

**AI Tasks**:
- Text generation (7 Wh per paragraph)
- Code generation (0.5 Wh per 100 lines)
- Image generation (2 Wh per 1024x1024 image)
- Video generation from text (500 Wh per 3-second clip)
- Video generation from image (650 Wh per 3-second clip)

**Data & Cloud Tasks**:
- Google search (0.3 Wh per search)
- Smartphone charging (20 Wh per full charge)
- Cloud photo storage (8 Wh per 1000 photos/month)
- Netflix streaming (200 Wh per hour)
- Video calling (2000 Wh per hour with 10 people)

## Setup Instructions

### Prerequisites
- [Conda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) installed

### Installation

1. **Clone or download this project**
   ```bash
   # If using git
   git clone <your-repo-url>
   cd <project-directory>
   ```

2. **Create the Conda environment**
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the environment**
   ```bash
   conda activate energy-calculator
   ```

4. **Run the Streamlit apps**
   
   **Single Country Calculator:**
   ```bash
   streamlit run app.py
   ```
   
   **Country Comparison Tool:**
   ```bash
   streamlit run compare_app.py
   ```

5. **Open your browser**
   The apps will automatically open at `http://localhost:8501` (or the next available port)

### Alternative Setup (if you prefer pip)

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas plotly kaleido

# Run the app
streamlit run app.py
```

## Usage

1. **Select Your Location**: Choose your electrical grid location from the dropdown
2. **Configure Usage**: Enter quantities for different AI and cloud tasks
3. **View Results**: See total energy consumption, carbon impact, and comparisons
4. **Compare Locations**: Understand how the same activities impact differently across regions

## Energy Data Sources

The energy consumption values are based on research estimates for typical AI and cloud computing tasks:

- **AI Tasks**: Text generation (7 Wh), code generation (0.5 Wh), image generation (2 Wh), video generation (500-650 Wh)
- **Cloud Tasks**: Search (0.3 Wh), smartphone charging (20 Wh), cloud storage (8 Wh/month), streaming (200 Wh/hour), video calls (2000 Wh/hour)

## Grid Carbon Intensity Sources

Carbon intensity values are 2023 averages from national grid operators and energy agencies.

## Troubleshooting

**Environment creation fails:**
```bash
# Update conda first
conda update conda
conda env create -f environment.yml
```

**Port already in use:**
```bash
# Run on a different port
streamlit run app.py --server.port 8502
```

**Package conflicts:**
```bash
# Remove and recreate environment
conda env remove -n energy-calculator
conda env create -f environment.yml
```

## Contributing

Feel free to submit issues or pull requests to improve the energy data accuracy or add new features!
