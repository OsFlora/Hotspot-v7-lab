#!/usr/bin/env bash

# Remove results from previous simulations
rm -f *.init
rm -f outputs/*

# Create outputs directory if it doesn't exist
mkdir outputs

# HotSpot's grid model is capable of modeling stacked 3-D chips. To be
# able to do that, one has to specify what is called the 'Layer
# Configuration File' (LCF). An LCF specifies the set of vertical layers
# to be modeled including its physical properties (thickness,
# conductivity etc.) and the floorplan of the die in that layer.

# Let us now look at an example of how to model stacked 3-D chips. Let
# us use a simple, 3-block floorplan file 'floorplan1.flp' in addition to
# the more detailed original 'floorplan2.flp'. In the chip we will model, layer 0 is
# power dissipating silicon with a floorplan of 'floorplan1.flp', followed
# by a layer of non-dissipating (passive) TIM. This is then followed by
# another layer of active silicon with a floorplan of 'floorplan2.flp' and
# another layer of passive TIM. Such a layer configuration is described
# in 'example.lcf'. Note that the floorplan files of all layers are specified
# in the LCF instead of via the command line
../../hotspot -c example.config -p example.ptrace -grid_layer_file example.lcf -materials_file example.materials -model_type grid -detailed_3D on -steady_file outputs/example.steady -grid_steady_file outputs/example.grid.steady
# Copy steady-state results over to initial temperatures
cp outputs/example.steady example.init

# Transient simulation
../../hotspot -c example.config -p example.ptrace -grid_layer_file example.lcf -materials_file example.materials -model_type grid -detailed_3D on -o outputs/example.ttrace -grid_transient_file outputs/example.grid.ttrace

# Visualize Heat Map of Layer 0 with Perl and with Python script
../../scripts/split_grid_steady.py outputs/example.grid.steady 6 64 64
../../scripts/grid_thermal_map.py floorplan2.flp outputs/example_layer2.grid.steady 64 64 outputs/layer2.png
../../scripts/grid_thermal_map.pl floorplan2.flp outputs/example_layer2.grid.steady 64 64 > outputs/layer2.svg

# Task3
# 3D stacking simulation (Grid + detailed 3D)
../../hotspot -c example.config -p example.ptrace -grid_layer_file example.lcf -materials_file example.materials -model_type grid -detailed_3D on -steady_file outputs/3d_steady.steady -grid_steady_file outputs/3d_grid.steady

# Split per-layer temperature (assuming 6 layers; adjust from .lcf)
python3 ../../scripts/split_grid_steady.py outputs/3d_grid.steady 6 64 64

# Visualize the selected layers
python3 ../../scripts/grid_thermal_map.py floorplan1.flp outputs/3d_grid_layer0.grid.steady 64 64 outputs/layer0_heatmap.png
python3 custom_grid_thermal_map.py floorplan1.flp outputs/3d_grid_layer0.grid.steady 64 64 50 110 outputs/layer0_heatmap_celsius.png

python3 ../../scripts/grid_thermal_map.py floorplan2.flp outputs/3d_grid_layer2.grid.steady 64 64 outputs/layer2_heatmap.png
python3 custom_grid_thermal_map.py floorplan2.flp outputs/3d_grid_layer2.grid.steady 64 64 50 110 outputs/layer2_heatmap_c

# Compare with 2D simulation (Grid without detailed 3D)
# The result is printed in termal
cd $HOTSPOT/examples/example1
../../hotspot -c example.config -f ev6.flp -p gcc.ptrace -materials_file example.materials -model_type grid -grid_steady_file outputs/2d_grid.steady
python3 $HOTSPOT/examples/example3/extract_peak_temp.py outputs/2d_grid.steady

cd $HOTSPOT/examples/example3
python3 $HOTSPOT/examples/example3/extract_peak_temp.py outputs/3d_steady.steady
