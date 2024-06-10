import os, sys
import shutil
import re
import codecs

# functions
def remove_bom(file_path):
    BUFSIZE = 4096
    BOMLEN = len(codecs.BOM_UTF8)

    with open(file_path, "r+b") as fp:
        chunk = fp.read(BUFSIZE)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[BOMLEN:]
            while chunk:
                fp.seek(i)
                fp.write(chunk)
                i += len(chunk)
                fp.seek(BOMLEN, os.SEEK_CUR)
                chunk = fp.read(BUFSIZE)
            fp.seek(-BOMLEN, os.SEEK_CUR)
            fp.truncate()

# MAIN

if len(sys.argv) != 3:
    print("Usage: python getFiles.py </sourceDir> <referenceFile.csv>")
    sys.exit(1)

# args
source_dir = sys.argv[1]
output_dir = "out"
referenceFile = sys.argv[2]
keyColumnName = "StudentNumber"

# prep files and output dir
remove_bom(referenceFile)
shutil.rmtree(output_dir)
os.mkdir(output_dir)

# extract keys from .csv
with open(sys.argv[2]) as f:
    lines = f.readlines()
    lines = [line.split(",") for line in lines]
try:
    keyIndex = lines[0].index(keyColumnName)
except:
    print(f"{referenceFile} does not contain a \"{keyColumnName}\" column, please double check this column is named correctly")
    sys.exit(1)
keys = [line[keyIndex] for line in lines]
keys.pop(0)


missingkeys = []
foundfiles = []
# get lists of missing/present files
for key in keys:
    regex = re.compile(f'.*{key}.*')
    source = ""
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if regex.match(file):
                print(f"file containing key:{key} found, using: {file}")
                source = os.path.join(source_dir, file)
                break

    # error handling if no feedback file
    if len(source) == 0:
        missingkeys.append(key)
        continue

    foundfiles.append(source)

# copy files into new dir
for file in foundfiles:
    shutil.copy2(file,output_dir)

print("could not find files matching the following keys:\n" + str(missingkeys))