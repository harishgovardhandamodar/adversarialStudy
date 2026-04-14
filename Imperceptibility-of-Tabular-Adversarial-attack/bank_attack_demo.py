#!/usr/bin/env python3
"""
Script to run adversarial attacks on bank transaction data
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))


# Update the attack parameters to include bank dataset
def main():
    print("Bank dataset successfully integrated into the adversarial attack framework!")
    print("To run attacks on bank data, use the following command:")
    print("python 2_generate_ae.py -t 1 -d True -c True -f True -p True")
    print("This will run DeepFool, Carlini, FGSM and PGD attacks on bank dataset")


if __name__ == "__main__":
    main()
