import os

# Define the directory to search for files
directory = "./"

# Loop through all directories in the directory and subdirectories
for root, dirs, files in os.walk(directory):
    for d in dirs:
        # Check if the directory ends with "snap"
        if d.endswith("snap"):
            # Construct the file path to search for the "lsdev.adapter" file under the "general" directory
            filepath = os.path.join(root, d, "general", "lsdev.adapter")
            # Check if the file exists
            if os.path.exists(filepath):
                # Print the file path
                print("File path:", filepath)
                # Open the file and read its contents
                with open(filepath, "r") as f:
                    # Output the file contents
                    print(f.read())
                # Print a blank line to separate the output for each file
                print()
