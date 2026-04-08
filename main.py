# gFetch v.0.11.0 by mikeph52 4/4/2026
import subprocess
import requests
import json
import sys # for aborting connection and argv
from rich.table import Table
from rich.console import Console

# main tui window
console = Console() 

# Functions
def msg():
    print("gFetch v.0.11.0 by mikeph52\n")
    print("A better version of datasets\n")
    print("Using NCBI datasets (O'Leary NA et. al, 2024)")
    print("by the National Center for Biotechnology Information\n\n")

def help_me():
    # FIX HELP ME
    print("Usage: gfetch [mode] [type]-genome/-gene/-virus <taxon>")
    print("Modes: download/summary")
    print("Types: -genome/-gene/-virus\n\n")
    print("For more information, visit the github page https://github.com/mikeph52/gfetch.")

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
def NCBIdownGenome(taxon):
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

def NCBIdownGene(taxon):
    subprocess.run(["datasets","download","gene","taxon",taxon])

def NCBIdownVirus(taxon):
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

def display_genome_summary(data):
    table = Table(title="Genomic Summary", style="cyan")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("Organism", data["organism"]["organism_name"])
    table.add_row("Taxon ID", str(data["organism"]["tax_id"]))
    table.add_row("Accession", data["accession"])
    table.add_row("Assembly", data["assembly_info"]["assembly_name"])
    table.add_row("Level", data["assembly_info"]["assembly_level"])
    table.add_row("Release Date", data["assembly_info"]["release_date"])
    console.print(table)

# main logic
def startup():
    msg()
    CheckConnection()

def handle_download():
    if len(sys.argv) < 4:
        print("Usage: gfetch download -genome/-gene/-virus <taxon>")
        sys.exit(1)

    data_type = sys.argv[2]
    taxon = sys.argv[3]

    if data_type == "-genome":
        NCBIdownGenome(taxon)
    elif data_type == "-gene":
        NCBIdownGene(taxon)
    elif data_type == "-virus":
        NCBIdownVirus(taxon)
    else:
        print(f"Unknown type: {data_type}")
        sys.exit(1)

def handle_summary():
    if len(sys.argv) < 4:
        print("Usage: gfetch summary -genome/-gene/-virus <taxon>")
        sys.exit(1)

    data_type = sys.argv[2]
    taxon = sys.argv[3]

    if data_type == "-genome":
        print("Do you want only reference genomes? [y/n]")
        choice_ref = input()
        if choice_ref == "y":
            result = subprocess.run(
                ["datasets", "summary", "genome", "taxon", taxon,"--reference" ,"--as-json-lines"],
                capture_output=True, text=True)
        elif choice_ref == "n":
            result = subprocess.run(
                ["datasets", "summary", "genome", "taxon", taxon, "--as-json-lines"],
                capture_output=True, text=True)
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            data = json.loads(line)
            display_genome_summary(data)

    elif data_type == "-gene":
        result = subprocess.run(["datasets", "summary", "gene", "taxon", taxon,"--as-json-lines"],
                capture_output=True, text=True)
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            data = json.loads(line)
            display_genome_summary(data)
    
    elif data_type == "-virus":
        result = subprocess.run(["datasets", "summary", "virus", "taxon", taxon,"--as-json-lines"],
                capture_output=True, text=True)
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            data = json.loads(line)
            display_genome_summary(data)   
    else:
        print(f"Unknown type: {data_type}")
        sys.exit(1)

# main function
def main():
    if len(sys.argv) < 2:
        msg()
        print("Usage: gfetch [function] [type]-genome/-gene/-virus <taxon>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "download":
        startup()
        handle_download()
    elif command == "summary":
        startup()
        handle_summary()
    elif command == "help":
        msg()
        help_me()
    else:
        msg()
        print(f"Unknown command: {command}")
        print("   Run 'python gfetch.py help' for usage.")
        sys.exit(1)
        
if __name__ == "__main__":
    main()