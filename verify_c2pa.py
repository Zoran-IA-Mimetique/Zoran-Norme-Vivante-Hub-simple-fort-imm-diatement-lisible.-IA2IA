#!/usr/bin/env python3
import sys, json, glob
for path in sys.argv[1:]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            json.load(f)
        print("C2PA-like JSON OK:", path)
    except Exception as e:
        print("WARN:", path, e)
