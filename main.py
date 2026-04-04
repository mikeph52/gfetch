# gFetch v.0.0.1 by mikeph52 3/4/2026
import json
import subprocess
import requests


def help():
    print("gFetch v.0.0.1 by mikeph52\n")
    print("A better version of datasets\n\n")

    print("Using NCBI")
    subprocess.run(["datasets","--version"])

def NetworkTestNCBI():
    try:
        response = requests.get(
            "https://api.ncbi.nlm.nih.gov/datasets/v2/version",
            timeout=5
        )
        if response.status_code == 200:
            #print("NCBI API is reachable")
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
            #print("Internet connection is working")
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
    NetworkTestNCBI()
    NetworkTestGlobal()
    print("All ok")


def main():
    print("test")
    CheckConnection()


if __name__ == "__main__":
    main()