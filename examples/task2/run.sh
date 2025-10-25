#!/usr/bin/env bash

# Remove results from previous simulations
rm -f outputs/*

# Create outputs directory if it doesn't exist
mkdir -p outputs/

# Prepare floorplans A and B
# A: dispersed high‑power cores
# B: concentrated high‑power cores

# Visualize floorplans
echo "Generating floorplan visualizations..."
python3 ../../scripts/visualize_floorplan.py floorplan_A.flp ./outputs/floorplan_A_with_names.png
python3 ../../scripts/visualize_floorplan.py --without-names floorplan_A.flp ./outputs/floorplan_A_without_names.png

python3 ../../scripts/visualize_floorplan.py floorplan_B.flp ./outputs/floorplan_B_with_names.png
python3 ../../scripts/visualize_floorplan.py --without-names floorplan_B.flp ./outputs/floorplan_B_without_names.png
echo "Floorplan visualizations generated."

# Run simulations for both floorplans
# Run Block Model
../../hotspot -c task2.config -f floorplan_A.flp -p workload.ptrace -model_type block -materials_file example.materials  -steady_file outputs/A_block.steady
../../hotspot -c task2.config -f floorplan_B.flp -p workload.ptrace -model_type block -materials_file example.materials -steady_file outputs/B_block.steady

# Run Grid Model
../../hotspot -c task2.config -f floorplan_A.flp -p workload.ptrace -model_type grid -materials_file example.materials  -steady_file outputs/A_grid.steady -grid_steady_file outputs/A_grid.grid.steady
../../hotspot -c task2.config -f floorplan_B.flp -p workload.ptrace -model_type grid -materials_file example.materials  -steady_file outputs/B_grid.steady -grid_steady_file outputs/B_grid.grid.steady

# Block Model Heatmaps  
python3 simple_block_heatmap.py floorplan_A.flp outputs/A_block.steady outputs/A_block_heatmap.png --vmin 50 --vmax 100 --title "Floorplan A - Block Model" --kelvin
python3 simple_block_heatmap.py floorplan_B.flp outputs/B_block.steady outputs/B_block_heatmap.png --vmin 50 --vmax 100 --title "Floorplan B - Block Model" --kelvin

# Grid Model Heatmaps
# Split grid steady file into layers, then can use script to generate heatmap
python3 ../../scripts/split_grid_steady.py outputs/A_grid.grid.steady 4 64 64
python3 ../../scripts/split_grid_steady.py outputs/B_grid.grid.steady 4 64 64
# only generate silicon function layer 0 heatmap for brevity
# original scripts generate Kelvin temperature heatmap
# here we generate Celsius temperature heatmap
python3 ../../scripts/grid_thermal_map.py floorplan_A.flp outputs/A_grid_layer0.grid.steady 64 64 outputs/A_grid_layer0_heatmap.png 
python3 custom_grid_thermal_map.py floorplan_A.flp outputs/A_grid.grid.steady 64 64 50 100 outputs/A_custom_grid_heatmap_range.png 
python3 ../../scripts/grid_thermal_map.py floorplan_B.flp outputs/B_grid_layer0.grid.steady 64 64 outputs/B_grid_layer0_heatmap.png
python3 custom_grid_thermal_map.py floorplan_B.flp outputs/B_grid.grid.steady 64 64 50 100 outputs/B_custom_grid_heatmap_range.png

# Create peak‑temperature table for 4 layers
python3 create_peak_table.py outputs/A_block.steady outputs/B_block.steady outputs/A_grid.steady outputs/B_grid.steady outputs/peak_temp_table.csv  
