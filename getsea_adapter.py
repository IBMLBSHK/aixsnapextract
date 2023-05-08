import os
import json

# Remove any files *.json
# Directory path
dir_path = '.'
# Iterate over all files in the directory
for filename in os.listdir(dir_path):
    # Check if the file is a JSON file
    if filename.endswith('.json'):
        # Construct the full file path
        file_path = os.path.join(dir_path, filename)
        # Remove the file
        os.remove(file_path)
#Get all files in current directory that end with ".log"
log_files = [f for f in os.listdir('.') if f.endswith('.log')]

for log_file in log_files:
    with open(log_file, 'r') as f:
        lines = f.readlines()
    sea_list = {}
    print(log_file)
    # Extract information from lines that begin with "SEA :"
    for i, line in enumerate(lines):
        if line.startswith("SEA :"):
            sea_grep = line.strip()
            words_sea = sea_grep.split()
            if_name = words_sea[2]
            sea_list[if_name] = {}
            sea_list[if_name]['name'] = if_name
            
            continue
        elif "ETHERCHANNEL" in line:
            eadpt_grep = lines[i+3].strip()
            words_1 = eadpt_grep.split()

            #sea_list[if_name] = {}
            sea_list[if_name]['etherchannel'] = {}
            #sea_list[if_name]['name'] = if_name
            sea_list[if_name]['etherchannel']['name'] = words_1[0]
            sea_list[if_name]['etherchannel']['phy'] = words_1[1].split(',')
            sea_list[if_name]['etherchannel']['mode'] = words_1[2]
            sea_list[if_name]['etherchannel']['hash_mode'] = words_1[3]
            sea_list[if_name]['etherchannel']['jumbo'] = words_1[4]

            continue
        elif "REAL ADAPTERS" in line:
            # Get the length of the 'phy' list
            if 'etherchannel' in sea_list.get(if_name, {}) and 'phy' in sea_list[if_name]['etherchannel']:
                phy_list_length = len(sea_list[if_name]['etherchannel']['phy'])

            # Print the result
                print(f"There are {phy_list_length} elements in the 'phy' list.")
                if phy_list_length >= 1:
                    sea_list[if_name]['realadapter'] = []
                    for j in range(1,phy_list_length+1):
                        adpt_grep = lines[i+2+j].strip()
                        words_2 = adpt_grep.split()


                        
                        if len(words_2) <= 9:
                            while len(words_2) <= 10:
                                words_2.append("NA")
                        
                        print(words_2)
                        print(j)
                        
                        adapter_dict = {
                        'name': words_2[0],
                        'slot': words_2[1],
                        'hardware_path': words_2[2],
                        'link': words_2[3],
                        'selected_speed': words_2[4],
                        'running_speed': words_2[5],
                        'actor_system': words_2[6],
                        'actor_sync': words_2[7],
                        'partner_system': words_2[8],
                        'partner_port': words_2[9],
                        'partner_sync': words_2[10]
                        }
                        # Add the real adapter dictionary to the 'realadapter' list
                        sea_list[if_name]['realadapter'].append(adapter_dict)
                        
            else:
                adpt_grep = lines[i+3].strip()
                words_2 = adpt_grep.split()
                sea_list[if_name]['realadapter'] = {}
                ##sea_list[if_name] = {}
                #sea_list[if_name]['realadapter'] = {}
                #sea_list[if_name]['name'] = if_name
                sea_list[if_name]['realadapter']['name'] = words_2[0]
                sea_list[if_name]['realadapter']['slot'] = words_2[1]
                sea_list[if_name]['realadapter']['hardware_path'] = words_2[2]
                sea_list[if_name]['realadapter']['link'] = words_2[3]
                sea_list[if_name]['realadapter']['selected_speed'] = words_2[4]
                sea_list[if_name]['realadapter']['running_speed'] = words_2[5]

                
            
            continue
        if "VIRTUAL ADAPTERS" in line:
            vadpt_grep = lines[i+3].strip()
            words_3 = vadpt_grep.split()
            
            sea_list[if_name]['vadapter'] = {}
            sea_list[if_name]['vadapter']['name'] = words_3[0]
            sea_list[if_name]['vadapter']['slot'] = words_3[1]
            sea_list[if_name]['vadapter']['hardware_path'] = words_3[2]
            sea_list[if_name]['vadapter']['priority'] = words_3[3]
            sea_list[if_name]['vadapter']['active'] = words_3[4]
            sea_list[if_name]['vadapter']['port_vlan_id'] = words_3[5]
            sea_list[if_name]['vadapter']['vswitch'] = words_3[6]
            sea_list[if_name]['vadapter']['mode'] = words_3[7]
            if len(words_3) >= 9:
                sea_list[if_name]['vadapter']['vlan_tags_ids'] = words_3[8]
            else:
                sea_list[if_name]['vadapter']['vlan_tags_ids'] = "NA"
                                
            continue  

    # Check if a JSON file with the same name as the log file exists
    json_file = log_file + '_adapter.json'
    if not os.path.isfile(json_file) or os.path.getsize(json_file) == 0:
        # If the file is empty or does not exist, write sea_list to it
        with open(json_file, 'w') as f:
            json.dump(sea_list, f)
    else:
        # If the file exists and is not empty, append sea_list to it
        with open(json_file, 'r+') as f:
            data = json.load(f)
            data.update(sea_list)
            f.seek(0)
            json.dump(data, f)

    # Move this print statement outside the innermost loop
    print("JSON files updated")
