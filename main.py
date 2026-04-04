# gFetch v.0.2.0 by mikeph52 4/4/2026
import subprocess
import requests
import json

# Functions
def help():
    print("gFetch v.0.2.0 by mikeph52\n")
    print("A better version of datasets\n\n")

    print("Using NCBI")
    subprocess.run(["datasets","--version"])

# Network Diagnostics
def NetworkTestNCBI():
    try:
        response = requests.get(
            "https://api.ncbi.nlm.nih.gov/datasets/v2/version",
            timeout=5
        )
        if response.status_code == 200:
            print("NCBI API [OK]")
            #print(f"   Version: {response.json()}")
            return True
        else:
            print(f"Unexpected status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("No connection to NCBI API")
    except requests.exceptions.Timeout:
        print("Connection timed out")

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
    NetworkTestGlobal()
    NetworkTestNCBI()
    print("Net diagnostics [OK]\n")

def getTaxon():
    print("Enter the taxon number: ")
    taxon = input()
    return taxon

#ncbi
def NCBIDownload():
    #datasets download genome taxon 6656  --reference --dehydrated --filename "$DB"/arthropoda/arthropoda.zip --no-progressbar      
    taxon = "4932"
    subprocess.run(["datasets","download","genome","taxon",taxon,"--reference"])

def NCBIDehydrated(taxon):
    #taxon = "4932"
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
    
# main function
def main():
    taxon = getTaxon()
    help()
    print("THIS IS A TEST VERSION!!!\n")
    CheckConnection()
    NCBIDehydrated(taxon)

if __name__ == "__main__":
    main()