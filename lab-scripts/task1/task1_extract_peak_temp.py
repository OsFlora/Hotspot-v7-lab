#!/usr/bin/env python3

import sys
import os
import re
import glob

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

def get_power_from_filename(filename):
    """Extract power value from filename like gcc_p80.steady -> 80"""
    match = re.search(r'p(\d+)\.steady$', filename)
    if match:
        return int(match.group(1))
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 task1_extract_peak_temp.py <steady_file_or_directory>")
        sys.exit(1)
        
    path = sys.argv[1]
    
    # Check if it's a directory or file
    if os.path.isdir(path):
        # Process all .steady files in directory
        steady_files = glob.glob(os.path.join(path, "*.steady"))
        results = []
        
        for file_path in steady_files:
            peak_temp, peak_unit = extract_peak_temperature_with_unit(file_path)
            power = get_power_from_filename(os.path.basename(file_path))
            
            if peak_temp is not None and peak_unit is not None and power is not None:
                results.append((power, peak_temp, peak_unit, os.path.basename(file_path)))
                # Convert K to C
                temp_c = peak_temp - 273.15
                print(f"{os.path.basename(file_path)} {power} {peak_temp:.2f} {peak_unit} {temp_c:.2f}")
        
        # Sort by power
        results.sort(key=lambda x: x[0])
        
        # Save results to a file
        with open("peak_temperatures.txt", "w") as f:
            for power, temp_k, unit, filename in results:
                temp_c = temp_k - 273.15
                f.write(f"{power} {temp_k:.2f} {unit} {temp_c:.2f}\n")
                
    else:
        # Process single file
        peak_temp, peak_unit = extract_peak_temperature_with_unit(path)
        power = get_power_from_filename(os.path.basename(path))
        
        if peak_temp is not None and peak_unit is not None and power is not None:
            temp_c = peak_temp - 273.15
            print(f"{os.path.basename(path)} {power} {peak_temp:.2f} {peak_unit} {temp_c:.2f}")
        else:
            print("Failed to extract peak temperature")

if __name__ == "__main__":
    main()