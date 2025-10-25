#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import numpy as np

def read_floorplan(filename):
    blocks = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) >= 5:
                name = parts[0]
                width = float(parts[1])
                height = float(parts[2])
                left_x = float(parts[3])
                bottom_y = float(parts[4])
                blocks.append((name, width, height, left_x, bottom_y))
    return blocks

def read_temperatures(filename):
    temps = {}
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    name = parts[0]
                    temp = float(parts[1])
                    temps[name] = temp
    return temps

def draw_heatmap(blocks, temperatures, output_file, vmin=50, vmax=100, title="", kelvin=False):
    # Convert temperatures from Kelvin to Celsius if needed
    if kelvin:
        temperatures = {name: temp - 273.15 for name, temp in temperatures.items()}
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Collect valid blocks (those with temperature data)
    valid_blocks = []
    temps = []
    
    for block in blocks:
        name, width, height, left_x, bottom_y = block
        if name in temperatures:
            valid_blocks.append(block)
            temps.append(temperatures[name])
    
    # Draw blocks
    for block, temp in zip(valid_blocks, temps):
        name, width, height, left_x, bottom_y = block
        rect = plt.Rectangle((left_x, bottom_y), width, height, 
                           facecolor=plt.cm.RdYlBu_r((temp-vmin)/(vmax-vmin)),
                           edgecolor='black', linewidth=0.5)
        ax.add_patch(rect)
        # Add label
        # temp_unit = "°C" if not kelvin else "K"  # Show original unit in label
        temp_display = temp   # Show original value in label
        plt.text(left_x + width/2, bottom_y + height/2, f'{name}\n{temp_display:.1f}{"°C"}',
                ha='center', va='center', fontsize=8, 
                bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.7))
    
    # Set axis limits based on blocks
    if valid_blocks:
        min_x = min(b[3] for b in valid_blocks)
        max_x = max(b[3] + b[1] for b in valid_blocks)
        min_y = min(b[4] for b in valid_blocks)
        max_y = max(b[4] + b[2] for b in valid_blocks)
        
        # Add some padding
        x_pad = (max_x - min_x) * 0.05
        y_pad = (max_y - min_y) * 0.05
        
        ax.set_xlim(min_x - x_pad, max_x + x_pad)
        ax.set_ylim(min_y - y_pad, max_y + y_pad)
    
    ax.set_aspect('equal')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title(title)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlBu_r, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Temperature (°C)')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 simple_block_heatmap.py <floorplan_file> <temperature_file> <output_file> [--vmin <value>] [--vmax <value>] [--title <title>] [--kelvin]")
        sys.exit(1)
    
    floorplan_file = sys.argv[1]
    temperature_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # Default values
    vmin = 50
    vmax = 100
    title = ""
    kelvin = False
    
    # Parse optional arguments
    i = 4
    while i < len(sys.argv):
        if sys.argv[i] == '--vmin' and i+1 < len(sys.argv):
            vmin = float(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '--vmax' and i+1 < len(sys.argv):
            vmax = float(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '--title' and i+1 < len(sys.argv):
            title = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == '--kelvin':
            kelvin = True
            i += 1
        else:
            i += 1
    
    # Read data
    blocks = read_floorplan(floorplan_file)
    temperatures = read_temperatures(temperature_file)
    
    # Draw heatmap
    draw_heatmap(blocks, temperatures, output_file, vmin, vmax, title, kelvin)
    print(f"Heatmap saved to {output_file}")

if __name__ == "__main__":
    main()