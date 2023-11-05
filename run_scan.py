
import argparse
from network_scanner_class import NetworkScanner

def main():
    scanner = NetworkScanner()
    scanner.scan_async()

if __name__ == "__main__":
    main()
