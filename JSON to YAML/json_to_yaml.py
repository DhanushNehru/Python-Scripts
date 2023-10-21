# script to convert json to yaml
import json
import os
import sys
import yaml
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        sourcefile = open(sys.argv[1], "r")
        contentsource = json.load(sourcefile)
        sourcefile.close()
    else:
        print("ERROR: " + sys.argv[1] + " not found")
        exit(1)
else:
    print("Usage: json2yaml.py <sourcefile.json> [target_file.yaml]")
outs = yaml.dump(contentsource)
if len(sys.argv) < 3:
    print(outs)
elif os.path.exists(sys.argv[2]):
    print("ERROR: " + sys.argv[2] + " already exists")
    exit(1)
else:
    target_file = open(sys.argv[2], "w")
    target_file.write(outs)
    target_file.close()
##end