import os

# Define the directory to search for files
directory = "./"

# Loop through all directories in the directory and subdirectories
for root, dirs, files in os.walk(directory):
    for d in dirs:
        # Check if the directory ends with "snap"
        if d.endswith("snap"):
            # Construct the file path to search for the "nim.script" file under the "general/nim" directory
            filepath = os.path.join(root, d, "general", "nim", "nim.script")
            # Check if the file exists
            if os.path.exists(filepath):
                # Print the file path
                print("File path:", filepath)
                # Open the file and read its contents
                with open(filepath, "r") as f:
                    # Initialize the disk_names and disk_sizes arrays
                    disk_names = []
                    disk_sizes = []
                    # Loop through each line in the file contents
                    for line in f:
                        # Check if the line contains "lsmpio -ql hdisk"
                        if "lsmpio -ql hdisk" in line:
                            # Find the next line containing "Device:"
                            device_line = next((l for l in f if "Device:" in l), None)
                            if device_line:
                                # Extract the disk name from the line and add it to the disk_names array
                                disk_name = device_line.split()[-1]
                                # Find the line containing "Capacity:"
                                capacity_line = next((l for l in f if "Capacity:" in l), None)
                                if capacity_line:
                                    # Extract the disk size from the line and add it to the disk_sizes array
                                    disk_size = capacity_line.split()[-1]
                                    # Check if we need to stop searching
                                    if len(disk_names) > 0 and disk_name == disk_names[0]:
                                        break
                                    disk_names.append(disk_name)
                                    disk_sizes.append(disk_size)
                                    # Output the disk name and disk size
                                    print("Disk name:", disk_name)
                                    print("Disk size:", disk_size)
                        elif "entstat" in line:
                            # If the line contains "entstat", stop searching
                            break
                # Print a blank line to separate the output for each file
                print()
