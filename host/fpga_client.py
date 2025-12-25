# host/fpga_client.py
# Purpose: Simulate offloading math to the FPGA hardware
import numpy as np

def compute_on_fpga(weight, input_val):
    """
    Simulates sending data to the AXI-Stream Verilog Core.
    In a real system, this would use the PYNQ or XRT library.
    """
    # Hardware logic: result = weight * input_val
    # We use 16-bit fixed point simulation
    w_fixed = int(weight * 256) # Scaling for fixed-point
    i_fixed = int(input_val * 256)
    
    # Simulating the Verilog product_reg
    product = (w_fixed * i_fixed) / (256 * 256)
    
    print(f"[FPGA] Processed Input: {input_val} with Weight: {weight} -> Result: {product}")
    return product

if __name__ == "__main__":
    # Test the 'hardware' call
    result = compute_on_fpga(0.75, 2.4)
    print(f"Final Hardware-Accelerated Output: {result}")