#!/usr/bin/env python3

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection

def read_flp_file(flp_path):
    """Read floorplan file and return block information"""
    blocks = {}
    
    try:
        with open(flp_path, 'r') as f:
            for line in f:
                # Skip comments and empty lines
                if line.strip().startswith('#') or not line.strip():
                    continue
                
                # Parse block information
                parts = line.strip().split('\t')
                if len(parts) >= 5:
                    try:
                        name = parts[0]
                        width = float(parts[1])
                        height = float(parts[2])
                        left_x = float(parts[3])
                        bottom_y = float(parts[4])
                        
                        blocks[name] = {
                            'width': width,
                            'height': height,
                            'left_x': left_x,
                            'bottom_y': bottom_y
                        }
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Error: Floorplan file {flp_path} not found")
        return None
    except Exception as e:
        print(f"Error reading floorplan file {flp_path}: {e}")
        return None
        
    return blocks

def read_steady_file(steady_path):
    """Read steady state temperature file and return temperature data"""
    temperatures = {}
    
    try:
        with open(steady_path, 'r') as f:
            for line in f:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Parse temperature information
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    try:
                        name = parts[0]
                        temp_k = float(parts[1])
                        # Convert from Kelvin to Celsius
                        temp_c = temp_k - 273.15
                        temperatures[name] = temp_c
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"Error: Steady file {steady_path} not found")
        return None
    except Exception as e:
        print(f"Error reading steady file {steady_path}: {e}")
        return None
        
    return temperatures

def draw_heatmap(blocks, temperatures, output_file="heatmap.png", vmin=40, vmax=110, title="Temperature Heatmap"):
    """Draw heatmap of the floorplan with temperature data"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Collect all rectangles and temperatures
    rectangles = []
    temps = []
    
    # Find min and max coordinates for setting axis limits
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    
    for name, block in blocks.items():
        # Check if we have temperature data for this block
        if name in temperatures:
            # Create rectangle
            rect = patches.Rectangle(
                (block['left_x'], block['bottom_y']), 
                block['width'], 
                block['height']
            )
            rectangles.append(rect)
            temps.append(temperatures[name])
            
            # Update coordinate bounds
            min_x = min(min_x, block['left_x'])
            max_x = max(max_x, block['left_x'] + block['width'])
            min_y = min(min_y, block['bottom_y'])
            max_y = max(max_y, block['bottom_y'] + block['height'])
    
    # Create patch collection with colormap
    pc = PatchCollection(rectangles, cmap='hot', alpha=0.8)
    pc.set_array(np.array(temps))
    pc.set_clim(vmin=vmin, vmax=vmax)
    
    # Add collection to axes
    ax.add_collection(pc)
    
    # Add colorbar
    cbar = plt.colorbar(pc, ax=ax, shrink=0.8)
    cbar.set_label('Temperature (°C)', rotation=270, labelpad=20)
    
    # Add temperature labels on blocks
    for name, block in blocks.items():
        if name in temperatures:
            # Calculate center of block
            center_x = block['left_x'] + block['width'] / 2
            center_y = block['bottom_y'] + block['height'] / 2
            
            # Add temperature text
            ax.text(center_x, center_y, f'{temperatures[name]:.1f}°C', 
                   ha='center', va='center', fontsize=8, 
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.7))
    
    # Set axis properties
    ax.set_xlim(min_x - 0.001, max_x + 0.001)
    ax.set_ylim(min_y - 0.001, max_y + 0.001)
    ax.set_aspect('equal')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title(title)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Heatmap saved to {output_file}")
    plt.close()

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 task1_draw_block_heatmap.py <flp_file> <steady_file> [output_file] [--vmin VALUE] [--vmax VALUE] [--title TITLE]")
        print("Example: python3 task1_draw_block_heatmap.py ev6.flp gcc_p100.steady heatmap_p100.png --vmin 40 --vmax 110 --title \"Default Power(100%)\"")
        sys.exit(1)
        
    flp_file = sys.argv[1]
    steady_file = sys.argv[2]
    
    # Default values
    output_file = "heatmap.png"
    vmin = 40
    vmax = 110
    title = "Temperature Heatmap"
    
    # Parse optional arguments
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--vmin" and i + 1 < len(sys.argv):
            vmin = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--vmax" and i + 1 < len(sys.argv):
            vmax = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--title" and i + 1 < len(sys.argv):
            title = sys.argv[i + 1]
            i += 2
        elif not sys.argv[i].startswith("--"):
            output_file = sys.argv[i]
            i += 1
        else:
            i += 1
    
    # Read floorplan and temperature data
    blocks = read_flp_file(flp_file)
    temperatures = read_steady_file(steady_file)
    
    if blocks is None or temperatures is None:
        print("Failed to read input files")
        sys.exit(1)
    
    # Draw heatmap
    draw_heatmap(blocks, temperatures, output_file, vmin, vmax, title)

if __name__ == "__main__":
    main()