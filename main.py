# gFetch v.0.8.2 by mikeph52 4/4/2026
import subprocess
import requests
import json
import sys # for aborting connection

# Functions
def print_help():
    print("gFetch v.0.8.2 by mikeph52\n")
    print("A better version of datasets\n")
    print("Using NCBI datasets (O'Leary NA et. al, 2024)")
    print("by the National Center for Biotechnology Information\n\n")

# Network Diagnostics
def NetworkTestNCBI():
    try:
        response = requests.get(
            "https://api.ncbi.nlm.nih.gov/datasets/v2/version",
            timeout=5
        )
        if response.status_code == 200:
            print("NCBI API [OK]")
            return True
        else:
            print(f"Unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("No connection to NCBI API")
        return False
    except requests.exceptions.Timeout:
        print("Connection timed out")
        return False
def NetworkTestGlobal():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("Internet connection [OK]")
            return True
        else:
            print(f"Unexpected status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        return False
    except requests.exceptions.Timeout:
        print("Connection timed out")
        return False
def CheckConnection():
    print("Net diagnostics [CHECK]")
    print("-----------------------")
    if not NetworkTestGlobal():
        print("Internet connection [FAULT]")
        print("Aborting — no internet.")
        print("Net diagnostics [FAULT]")
        sys.exit(1)
    if not NetworkTestNCBI():
       print("NCBI API [FAULT]")
       print("Aborting - no connection to NCBI API")
       print("Net diagnostics [FAULT]")
       sys.exit(1)
    print("Net diagnostics [OK]")
    print("-----------------------\n")

# ncbi downloads
def NCBIdownGenome():
    print("Enter the taxon number: ")
    taxon = input()
    summary = subprocess.run(["datasets", "summary" ,"genome","taxon",taxon ,"--as-json-lines"],capture_output=True, text=True)
    
    sizes = []
    for line in summary.stdout.strip().split("\n"):
        if not line:
            continue
        d = json.loads(line)
        val = d.get('assembly_stats', {}).get('total_sequence_length', 0)
        sizes.append(int(val) if val else 0)

    sizeGB = sum(sizes)/1e9

    if sizeGB >= 10:
        subprocess.run(["datasets","download","genome","taxon",taxon,"--dehydrated","--reference"])
    else:
        subprocess.run(["datasets","download","genome","taxon",taxon,"--reference"])

def NCBIdownGene():
    print("Enter the taxon number: ")
    taxon = input()
    subprocess.run(["datasets","download","gene","taxon",taxon])

def NCBIdownVirus():
    print("Enter the taxon number: ")
    taxon = input()
    summary = subprocess.run(["datasets", "summary" ,"virus","genome","taxon",taxon ,"--as-json-lines"],capture_output=True, text=True)
    
    sizes = []
    for line in summary.stdout.strip().split("\n"):
        if not line:
            continue
        d = json.loads(line)
        val = d.get('assembly_stats', {}).get('total_sequence_length', 0)
        sizes.append(int(val) if val else 0)

    sizeGB = sum(sizes)/1e9

    if sizeGB >= 10:
        subprocess.run(["datasets","download","virus","genome","taxon",taxon,"--dehydrated"])
    else:
        subprocess.run(["datasets","download","virus","genome","taxon",taxon])

# ncbi summary
def NCBISumGenome():
    print("Enter the taxon number: ")
    taxon = input()
    subprocess.run(["datasets", "summary","genome","taxon",taxon])
def NCBISumGene():
    print("Enter the taxon number: ")
    taxon = input()
    subprocess.run(["datasets", "summary","gene","taxon",taxon])
def NCBISumVirus():
    print("Enter the taxon number: ")
    taxon = input()
    subprocess.run(["datasets", "summary","virus","genome","taxon",taxon])
    
# main logic
def startup():
    print_help()
    print("THIS IS A TEST VERSION!!!\n")
    CheckConnection()

def iftreeDownloads():
    print("Select function: -genome , -gene, -virus")
    x = input()
    if x == "-genome":
        NCBIdownGenome()
    elif x == "-gene":
        NCBIdownGene()
    elif x == "-virus":
        NCBIdownVirus()

def iftreeSummary():
    print("Select function: -genome , -gene, -virus")
    x = input()
    if x == "-genome":
        NCBISumGenome()
    elif x == "-gene":
        NCBISumGene()
    elif x == "-virus":
        NCBISumVirus()

# main function
def main():
    startup()
    print("Select mode: a)Download b)Summary")
    mode = input()
    if mode == "a":
        iftreeDownloads()
    elif mode == "b":
        iftreeSummary()
    else:
        print("Wrong input.")

if __name__ == "__main__":
    main()