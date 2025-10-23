#!/usr/bin/env python3

import sys
import os

def scale_power_values(input_file, output_file, scale_factor):
    """
    Scale all numeric values in a power trace file by a given factor.
    
    Args:
        input_file (str): Path to the input power trace file
        output_file (str): Path to the output power trace file
        scale_factor (float): Factor to multiply all numeric values by
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                # Skip empty lines
                if not line.strip():
                    outfile.write(line)
                    continue
                
                # Handle header line (first line with component names)
                if not any(char.isdigit() for char in line):
                    outfile.write(line)
                    continue
                
                # Process lines with numeric values
                values = line.strip().split('\t')
                scaled_values = []
                
                for value in values:
                    try:
                        # Convert to float, scale, and format back to string
                        num_value = float(value)
                        scaled_value = num_value * scale_factor
                        # Preserve the original format as much as possible
                        if '.' in value:
                            # If original had decimal point, keep similar precision
                            scaled_values.append(str(scaled_value))
                        else:
                            # If original was integer-like, format appropriately
                            scaled_values.append(str(scaled_value))
                    except ValueError:
                        # If conversion fails, keep original value
                        scaled_values.append(value)
                
                outfile.write('\t'.join(scaled_values) + '\n')
        
        print(f"Successfully scaled power values from {input_file} to {output_file} by factor {scale_factor}")
        
    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing files: {e}")
        sys.exit(1)

def generate_output_filename(input_file, scale_factor):
    """
    Generate output filename based on input filename and scale factor.
    
    Args:
        input_file (str): Path to the input file
        scale_factor (float): Scale factor
        
    Returns:
        str: Generated output filename
    """
    # Extract base name without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    # Format scale factor to remove trailing zeros
    scale_str = f"{scale_factor:g}"
    # Replace dots with p for filename compatibility
    scale_str = scale_str.replace('.', 'p')
    # Generate output filename
    output_file = f"{base_name}_{scale_str}.ptrace"
    return output_file

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scale_power.py <input_file> <scale_factor> [output_file]")
        print("Example: python3 scale_power.py gcc.ptrace 1.2")
        print("Example: python3 scale_power.py gcc.ptrace 0.8 gcc_p08.ptrace")
        sys.exit(1)
    
    input_file = sys.argv[1]
    try:
        scale_factor = float(sys.argv[2])
    except ValueError:
        print("Error: Scale factor must be a number.")
        sys.exit(1)
    
    # Determine output filename
    if len(sys.argv) >= 4:
        output_file = sys.argv[3]
    else:
        output_file = generate_output_filename(input_file, scale_factor)
    
    # Perform scaling
    scale_power_values(input_file, output_file, scale_factor)

if __name__ == "__main__":
    main()