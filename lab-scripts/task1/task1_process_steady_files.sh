#!/bin/bash

# Script to scale power traces, run hotspot simulations, extract peak temperatures and plot temp vs power graph

# SCALE USAGE EXAMPLES:
# python3 task1_scale_power.py gcc.ptrace 0.8 gcc_p08.ptrace
# python3 task1_scale_power.py gcc.ptrace 1.0 gcc_p10.ptrace
# python3 task1_scale_power.py gcc.ptrace 1.2 gcc_p12.ptrace

# Define paths
EXAMPLE_DIR="/fact_home/ruyisong/Tool/HotSpot/examples/example1"
OUTPUTS_DIR="$EXAMPLE_DIR/outputs"
LAB_SCRIPTS_DIR="/fact_home/ruyisong/Tool/HotSpot/lab-scripts"

echo "Processing HotSpot steady files..."

# Step 1: Extract peak temperatures
echo "Step 1: Extracting peak temperatures..."
cd $LAB_SCRIPTS_DIR
python3 task1_extract_peak_temp.py $OUTPUTS_DIR

# Check if extraction was successful
if [ ! -f "peak_temperatures.txt" ]; then
    echo "Error: Failed to extract peak temperatures"
    exit 1
fi

echo "Peak temperatures extracted to peak_temperatures.txt:"
cat peak_temperatures.txt

# Step 2: Plot temperature vs power
echo "Step 2: Plotting temperature vs power..."
python3 task1_plot_temp_vs_power.py peak_temperatures.txt

echo "Process completed successfully!"
echo "Generated files:"
echo "- peak_temperatures.txt"
echo "- temp_vs_power.png"