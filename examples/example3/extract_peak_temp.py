#!/usr/bin/env python3

import sys
import os

def extract_peak_temperature_with_unit(file_path):
    """Extract peak temperature and unit name from a .steady file"""
    max_temp = float('-inf')
    max_unit = ""
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # Split line into components
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    try:
                        temp = float(parts[1])
                        if temp > max_temp:
                            max_temp = temp
                            max_unit = parts[0]
                    except ValueError:
                        # Skip lines that don't have valid temperature values
                        continue
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None, None
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None, None
        
    return (max_temp, max_unit) if max_temp != float('-inf') else (None, None)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 extract_peak_temp.py <steady_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    # Process single file
    peak_temp, peak_unit = extract_peak_temperature_with_unit(file_path)
    
    if peak_temp is not None and peak_unit is not None:
        temp_c = peak_temp - 273.15
        print(f"{os.path.basename(file_path)}: Peak temperature = {peak_temp:.2f} K ({temp_c:.2f} °C) at unit {peak_unit}")
    else:
        print("Failed to extract peak temperature")

if __name__ == "__main__":
    main()