#!/usr/bin/env python3
from showroom.main import main
import os
import sys

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('[-] Interrupted, exiting program...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
