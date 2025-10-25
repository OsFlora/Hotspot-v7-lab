#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

usage = """
usage: custom_grid_thermal_map.py <flp_file> <grid_temp_file> <rows> <cols> <filename>.png (or)
       custom_grid_thermal_map.py <flp_file> <grid_temp_file> <rows> <cols> <min_temp> <max_temp> <filename>.png

Saves a heat map as a PNG image with the filename <filename>.png
Temperatures are automatically converted from Kelvin to Celsius.

<flp_file>       -- path to the file containing the floorplan (eg: example.flp)
<grid_temp_file> -- path to the grid temperatures file (eg: layer_0.grid.steady)
<rows>           -- no. of rows in the grid
<cols>           -- no. of columns in the grid
<min_temp>       -- min. temperature in Celsius (defaults to min. from <grid_temp_file>)
<max_temp>       -- max. temperature in Celsius (defaults to max. from <grid_temp_file>)
<filename>.png   -- output filename
"""

def read_floorplan(flp_filename):
    """Read floorplan file and return total dimensions"""
    total_width = -np.inf
    total_length = -np.inf
    
    with open(flp_filename, "r") as fp:
        for line in fp:
            # Ignore blank lines and comments
            if line == "\n" or line[0] == '#':
                continue

            parts = line.split()
            name = parts[0]
            width = float(parts[1])
            length = float(parts[2])
            x = float(parts[3])
            y = float(parts[4])

            total_width = max(total_width, x + width)
            total_length = max(total_length, y + length)
    
    return total_width, total_length

def read_grid_temperatures(temperatures_filename, rows, cols):
    """Read grid temperatures and return as 2D array in Celsius"""
    temps = []
    
    with open(temperatures_filename, "r") as fp:
        for line in fp:
            # Skip empty lines and lines with colons (like "Layer 0:")
            stripped_line = line.strip()
            if not stripped_line or ':' in stripped_line:
                continue
            
            # Extract temperature value (second field)
            parts = stripped_line.split()
            if len(parts) >= 2:
                try:
                    # Convert from Kelvin to Celsius
                    temp_celsius = float(parts[1]) - 273.15
                    temps.append(temp_celsius)
                except ValueError:
                    # Skip lines that can't be converted to float
                    continue

    # If we have multi-layer data, use only the first layer
    expected_values = rows * cols
    if len(temps) > expected_values:
        temps = temps[:expected_values]
    elif len(temps) < expected_values:
        print(f"Warning: Expected {expected_values} temperature values but got {len(temps)}")
        # Pad with zeros if we have fewer values
        temps.extend([0.0] * (expected_values - len(temps)))

    temps = np.reshape(temps, (rows, cols))
    return temps

def create_heatmap(flp_filename, temperatures_filename, rows, cols, output_filename, min_temp=None, max_temp=None):
    """Create heatmap from floorplan and temperature data"""
    # Read floorplan dimensions
    total_width, total_length = read_floorplan(flp_filename)
    
    # Read temperature data
    temps = read_grid_temperatures(temperatures_filename, rows, cols)
    
    # Create plot
    fig, axs = plt.subplots(1)
    
    # Draw floorplan outline
    with open(flp_filename, "r") as fp:
        for line in fp:
            # Ignore blank lines and comments
            if line == "\n" or line[0] == '#':
                continue

            parts = line.split()
            name = parts[0]
            width = float(parts[1])
            length = float(parts[2])
            x = float(parts[3])
            y = float(parts[4])

            rectangle = plt.Rectangle((x, y), width, length, fc="none", ec="black")
            axs.add_patch(rectangle)
            plt.text(x + width/2, y + length/2, name, ha='center', va='center', fontsize=8)
    
    # Create heatmap
    im = axs.imshow(temps, cmap='hot_r', extent=(0, total_width, 0, total_length))
    
    # Set temperature range
    if min_temp is None and max_temp is None:
        im.set_clim(np.min(temps), np.max(temps))
    else:
        if min_temp is None:
            min_temp = np.min(temps)
        if max_temp is None:
            max_temp = np.max(temps)
        im.set_clim(min_temp, max_temp)
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=axs)
    cbar.set_label('Temperature (°C)')
    
    # Set title with max temperature
    axs.set_title(f"Heat Map\nMaximum Temperature = {np.max(temps):.2f}°C")
    
    # Set axes labels
    axs.set_xticks([n for n in np.linspace(0, total_width, 5)])
    axs.set_xticklabels([f"{n*1000:.1f}" for n in np.linspace(0, total_width, 5)])
    axs.set_xlabel("Horizontal Position (mm)")
    
    axs.set_yticks([n for n in np.linspace(0, total_length, 5)])
    axs.set_yticklabels([f"{n*1000:.1f}" for n in np.linspace(0, total_length, 5)])
    axs.set_ylabel("Vertical Position (mm)")
    
    plt.axis('scaled')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Heatmap saved to {output_filename}")
    print(f"Temperature range: {np.min(temps):.2f}°C to {np.max(temps):.2f}°C")

def main():
    if len(sys.argv) == 6:
        flp_filename = sys.argv[1]
        temperatures_filename = sys.argv[2]
        rows = int(sys.argv[3])
        cols = int(sys.argv[4])
        output_filename = sys.argv[5]
        min_temp = None
        max_temp = None
    elif len(sys.argv) == 8:
        flp_filename = sys.argv[1]
        temperatures_filename = sys.argv[2]
        rows = int(sys.argv[3])
        cols = int(sys.argv[4])
        min_temp = float(sys.argv[5])
        max_temp = float(sys.argv[6])
        output_filename = sys.argv[7]
    else:
        print(usage)
        sys.exit(1)
    
    create_heatmap(flp_filename, temperatures_filename, rows, cols, output_filename, min_temp, max_temp)

if __name__ == "__main__":
    main()