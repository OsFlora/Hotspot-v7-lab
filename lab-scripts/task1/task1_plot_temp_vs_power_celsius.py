#!/usr/bin/env python3

import sys
import os
import matplotlib.pyplot as plt
import re

def parse_peak_temperatures_file(filepath):
    """Parse the peak temperatures file and extract Celsius temperatures"""
    powers = []
    temps_c = []
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    try:
                        power = int(parts[0])
                        temp_c = float(parts[3])  # Celsius temperature is now the 4th column
                        powers.append(power)
                        temps_c.append(temp_c)
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        return None, None
    except Exception as e:
        print(f"Error parsing file {filepath}: {e}")
        return None, None
        
    return powers, temps_c

def plot_temp_vs_power_celsius(powers, temps, output_file="temp_vs_power.png"):
    """Plot temperature vs power using Celsius"""
    plt.figure(figsize=(10, 6))
    plt.plot(powers, temps, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Power (W)', fontsize=12)
    plt.ylabel('Peak Temperature (°C)', fontsize=12)
    plt.title('Peak Temperature vs Power', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Add value labels on points
    for i, (power, temp) in enumerate(zip(powers, temps)):
        plt.annotate(f'{temp:.1f}°C', 
                    (power, temp), 
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {output_file}")
    plt.close()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 task1_plot_temp_vs_power_celsius.py <peak_temperatures_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    powers, temps_c = parse_peak_temperatures_file(input_file)
    
    if powers is not None and temps_c is not None:
        # Sort by power to ensure proper plotting
        sorted_data = sorted(zip(powers, temps_c))
        powers, temps_c = zip(*sorted_data)
        
        output_file = "temp_vs_power.png"
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
            
        plot_temp_vs_power_celsius(powers, temps_c, output_file)
    else:
        print("Failed to parse peak temperatures file")

if __name__ == "__main__":
    main()