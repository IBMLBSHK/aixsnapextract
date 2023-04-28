import os
import glob

# Define the directory to search for directories
directory = "./"

# Loop through all directories in the directory and subdirectories
for root, dirs, files in os.walk(directory):
    for d in dirs:
        # Check if the directory ends with "snap"
        if d.endswith("snap"):
            # Construct the file path to search for the "*vg.snap" file under the "lvm" directory
            filepath = os.path.join(root, d, "lvm", "*vg.snap")
            # Loop through all files matching the file path pattern
            for filename in glob.glob(filepath):
                # Open the file and read its contents
                with open(filename, "r") as f:
                    # Read the file contents
                    file_contents = f.read()
                    # Find the line containing the VG size and extract its value
                    for line in file_contents.splitlines():
                        if "TOTAL PPs:" in line:
                            print("File path:", filename)
                            vg_size_mb = int(line.split("(")[-1].split(")")[0].replace(" megabytes", ""))
                            vg_size_gb = vg_size_mb / 1024
                            # Print the VG size in gigabytes and the file path
                            print("VG size:", vg_size_gb, "GB")
                            
