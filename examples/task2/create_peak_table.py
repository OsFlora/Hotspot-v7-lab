#!/usr/bin/env python3

import sys
import os
import csv

def read_temperatures(filename):
    """Read temperature data from a HotSpot steady file"""
    temps = {}
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    name = parts[0]
                    temp = float(parts[1])
                    temps[name] = temp
    return temps

def create_peak_temperature_table(a_block_file, b_block_file, a_grid_file, b_grid_file, output_csv):
    """Create a peak temperature comparison table"""
    
    # Read all temperature data
    a_block_temps = read_temperatures(a_block_file)
    b_block_temps = read_temperatures(b_block_file)
    a_grid_temps = read_temperatures(a_grid_file)
    b_grid_temps = read_temperatures(b_grid_file)
    
    # Get all component names
    all_components = set()
    all_components.update(a_block_temps.keys())
    all_components.update(b_block_temps.keys())
    all_components.update(a_grid_temps.keys())
    all_components.update(b_grid_temps.keys())
    
    # Sort components for consistent ordering
    sorted_components = sorted(all_components)
    
    # Create CSV output
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow([
            "Component", 
            "A_Block_Temp_C", "B_Block_Temp_C",
            "A_Grid_Temp_C", "B_Grid_Temp_C"
        ])
        
        # Write data rows
        for component in sorted_components:
            # Get temperatures in Kelvin
            a_block_temp_k = a_block_temps.get(component)
            b_block_temp_k = b_block_temps.get(component)
            a_grid_temp_k = a_grid_temps.get(component)
            b_grid_temp_k = b_grid_temps.get(component)
            
            # Convert to Celsius (K - 273.15)
            a_block_temp_c = round(a_block_temp_k - 273.15, 2) if a_block_temp_k is not None else None
            b_block_temp_c = round(b_block_temp_k - 273.15, 2) if b_block_temp_k is not None else None
            a_grid_temp_c = round(a_grid_temp_k - 273.15, 2) if a_grid_temp_k is not None else None
            b_grid_temp_c = round(b_grid_temp_k - 273.15, 2) if b_grid_temp_k is not None else None
            
            # Format for CSV output (empty string for None values)
            row = [
                component,
                f"{a_block_temp_c:.2f}" if a_block_temp_c is not None else "",
                f"{b_block_temp_c:.2f}" if b_block_temp_c is not None else "",
                f"{a_grid_temp_c:.2f}" if a_grid_temp_c is not None else "",
                f"{b_grid_temp_c:.2f}" if b_grid_temp_c is not None else ""
            ]
            
            writer.writerow(row)
    
    print(f"Peak temperature table saved to {output_csv}")

def main():
    if len(sys.argv) != 6:
        print("Usage: python3 create_peak_table.py <A_block.steady> <B_block.steady> <A_grid.steady> <B_grid.steady> <peak_temp_table.csv>")
        sys.exit(1)
    
    a_block_file = sys.argv[1]
    b_block_file = sys.argv[2]
    a_grid_file = sys.argv[3]
    b_grid_file = sys.argv[4]
    output_csv = sys.argv[5]
    
    # Create peak temperature table
    create_peak_temperature_table(a_block_file, b_block_file, a_grid_file, b_grid_file, output_csv)

if __name__ == "__main__":
    main()