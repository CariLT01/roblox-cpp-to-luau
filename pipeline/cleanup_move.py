import sys
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--runpath", type=str)
parser.add_argument("--dist", type=str)

args = parser.parse_args()

run_path = args.runpath or "dist/src/server/run"
run_path_abs = os.path.abspath(run_path)

dist_path = args.dist or "dist"
dist_path_abs = os.path.abspath(dist_path)

if os.path.exists(run_path_abs) is False:
    raise SystemError(f"Run path not found: {run_path_abs}")
if os.path.exists(dist_path_abs) is False:
    raise SystemError(f"Dist path not found: {dist_path_abs}")


# Delete files

for file in os.listdir(run_path_abs):
    if not file.endswith(".lua"):
        continue
    print(f"Deleting: {file}")
    os.remove(os.path.join(run_path_abs, file))

# Find candidates
candidates: set[str] = set([])

for file in os.listdir(dist_path_abs):
    if not file.endswith(".min.luau"):
        continue
    
    candidates.add(os.path.join(dist_path_abs, file))
    

# Move
for candidate in candidates:
    
    name = os.path.basename(candidate)
    
    new_name = name.replace(".min.luau", ".lua")
    if name == "run.min.luau":
        new_name = "run.server.lua"
    
    os.rename(candidate, os.path.join(run_path_abs, new_name))
    print(f"Moved: {candidate}")
    