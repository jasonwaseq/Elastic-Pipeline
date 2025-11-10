import math
import numpy as np

def main():
    #xs = [i for i in list(range(128)) + list(range(-128, 0))]
    xs = [i for i in range(-128, 128)]
    os = [256 / (1 + math.exp(-x / 32)) for x in xs]

    # Convert each output to integer (0–255) and then to 2-digit hex
    hex_values = [hex(round(o))[2:] for o in os]

    # Write to output.hex file
    with open("sigmoid.hex", "w") as f:
        for val in hex_values:
            f.write(val + "\n")

    print("Success!!!")

if __name__ == "__main__":
    main()
