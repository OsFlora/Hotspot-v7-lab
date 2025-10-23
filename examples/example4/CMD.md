./grid_thermal_map.pl ev6_3D_core_layer.flp ./outputs/example.grid.steady 64  64 335 395 > out_enhanced.svg 


# split c
cd outputs && python3 ../../../scripts/split_grid_steady.py example.grid.steady 8 64 64

# plot
 python3 ../../../scripts/grid_thermal_map.py ../ev6_3D_core_layer.flp example_layer0.grid.steady 64 64 330 400 example_layer0.png
