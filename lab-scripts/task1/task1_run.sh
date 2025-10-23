#!/bin/bash

# Complete example script demonstrating the full workflow:
# 1. Scale power traces
# 2. Run hotspot simulations 
# 3. Extract peak temperatures
# 4. Plot temperature vs power

# Define paths
EXAMPLE_DIR="/fact_home/ruyisong/Tool/HotSpot/examples/example1"
OUTPUTS_DIR="$EXAMPLE_DIR/outputs"
LAB_SCRIPTS_DIR="/fact_home/ruyisong/Tool/HotSpot/lab-scripts/task1"
TASK_OUTPUTS_DIR="$LAB_SCRIPTS_DIR/results"
HOTSPOT_BIN="/fact_home/ruyisong/Tool/HotSpot/hotspot"
HOTFLOORPLAN_BIN="/fact_home/ruyisong/Tool/HotSpot/hotfloorplan"

rm -rf $TASK_OUTPUTS_DIR
mkdir -p $TASK_OUTPUTS_DIR
echo "=== HotSpot Analysis Workflow ==="

# Step 1: Scale power traces to different power levels
echo "Step 1: Scaling power traces..."
cd $LAB_SCRIPTS_DIR

# Scale to 80W, 100W, and 120W
python3 task1_scale_power.py $EXAMPLE_DIR/gcc.ptrace 0.8 $EXAMPLE_DIR/gcc_p80.ptrace
python3 task1_scale_power.py $EXAMPLE_DIR/gcc.ptrace 1.0 $EXAMPLE_DIR/gcc_p100.ptrace
python3 task1_scale_power.py $EXAMPLE_DIR/gcc.ptrace 1.2 $EXAMPLE_DIR/gcc_p120.ptrace

# Step 2: Run floorplanning (if needed)
# This step assumes floorplan already exists, but showing for completeness
# $HOTFLOORPLAN_BIN -f $EXAMPLE_DIR/example1.flp -p $EXAMPLE_DIR/gcc.ptrace

# Step 3: Run hotspot simulations for each power level
echo "Step 2: Running hotspot simulations..."
cd $EXAMPLE_DIR

# Run simulations (these would typically generate .steady and .ttrace files)
# You can walk in example1/run.sh for detailed files
bash run.sh

# Step 3: Extract peak temperatures
echo "Step 3: Extracting peak temperatures..."
cd $LAB_SCRIPTS_DIR
python3 task1_extract_peak_temp.py $OUTPUTS_DIR
cp peak_temperatures.txt $TASK_OUTPUTS_DIR/peak_temperatures.txt

echo "Peak temperatures extracted:"
echo "Power(W) Temperature(K) Unit_Name Temperature(C)"

# Step 4: Plot temperature vs power using Celsius
echo "Step 4: Plotting temperature vs power (Celsius)..."
python3 task1_plot_temp_vs_power_celsius.py peak_temperatures.txt
cp temp_vs_power.png $TASK_OUTPUTS_DIR/temp_vs_power.png

# Step 5: Draw heatmap for different power levels
echo "Step 5: Drawing heatmaps for different power levels..."
for power_level in 80 100 120; do
    python3 task1_draw_block_heatmap.py $EXAMPLE_DIR/ev6.flp $OUTPUTS_DIR/gcc_p${power_level}.steady $TASK_OUTPUTS_DIR/heatmap_p${power_level}.png --vmin 40 --vmax 80 --title "Default Power(${power_level}%)"
done

echo "=== Workflow completed successfully ==="
echo "Generated files:"
echo "- Scaled power traces in $EXAMPLE_DIR"
echo "- Peak temperatures in $$TASK_OUTPUTS_DIR/peak_temperatures.txt"
echo "- Temperature vs power plot in $TASK_OUTPUTS_DIR/temp_vs_power.png"