import os

# Get list of all directories ending with "snap"
snap_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d.endswith('snap')]

# Search for rootvg.snap files and extract rootvg size
rootvg_sizes = []

for snap_dir in snap_dirs:
    lvm_dir = os.path.join(snap_dir, 'lvm')
    if os.path.isdir(lvm_dir):
        rootvg_snap_file = os.path.join(lvm_dir, 'rootvg.snap')
        if os.path.isfile(rootvg_snap_file):
            with open(rootvg_snap_file, 'r') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if "TOTAL PPs:" in line:
                    rootvg_size_mb = int(line.split("(")[-1].split(")")[0].replace(" megabytes", ""))
                    rootvg_size_gb = rootvg_size_mb / 1024
                    rootvg_sizes.append({'file_directory': os.path.dirname(rootvg_snap_file),
                                         'rootvg_size': f"{rootvg_size_gb:.2f} GB"})
                    break

for rootvg_size in rootvg_sizes:
    print(f"File directory: {rootvg_size['file_directory']}")
    print(f"Rootvg size: {rootvg_size['rootvg_size']}")
