#!/usr/bin/env python3
import argparse
import subprocess

def run_timmy(datenmodell, eigenschaftsfile, sourcefile):
    command = ["timmy", f"--datenmodell={datenmodell}", f"--eigenschaftsfile={eigenschaftsfile}", sourcefile]
    result = subprocess.run(command, capture_output=True, text=True)
    print("Output:")
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)

def main():
    parser = argparse.ArgumentParser(description='Run timmy tool with specified options.')
    parser.add_argument('--datenmodell', required=True, help='Data model, e.g., lp64')
    parser.add_argument('--eigenschaftsfile', required=True, help='Path to the property file')
    parser.add_argument('sourcefile', help='Source file to analyze')

    args = parser.parse_args()
    run_timmy(args.datenmodell, args.eigenschaftsfile, args.sourcefile)

if __name__ == "__main__":
    main()
