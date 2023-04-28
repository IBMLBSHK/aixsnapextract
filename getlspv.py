import os

# Define the directory to search for files
directory = "./"

# Loop through all files in the directory and subdirectories
for root, dirs, files in os.walk(directory):
    for filename in files:
        # Check if the file ends with ".snap"
        if filename.endswith(".snap"):
            # Check if the file path contains "lvm/lvm.snap"
            if "lvm/lvm.snap" in os.path.join(root, filename):
                # Open the file and read its contents
                with open(os.path.join(root, filename), "r") as f:
                    # Read the file contents
                    file_contents = f.read()
                    # Find the index of the first occurrence of "hdisk"
                    start_index = file_contents.find("hdisk")
                    # Find the index of the first occurrence of "......" after the "hdisk" string
                    end_index = file_contents.find(".....", start_index)
                    # Print the substring between "hdisk" and "....."
                    print("File path:", os.path.join(root, filename))
                    print(file_contents[start_index:end_index])
