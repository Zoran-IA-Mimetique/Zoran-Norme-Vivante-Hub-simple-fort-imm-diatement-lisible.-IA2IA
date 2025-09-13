#!/usr/bin/env python3
import sys, yaml
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    yaml.safe_load(f)
print("YAML OK:", sys.argv[1])
