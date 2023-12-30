import os
import json

def save_json(data, filename):
    # save_directory = "services/epf-flower-data-science/src/data"
    # os.makedirs(save_directory, exist_ok=True)

    # filepath = os.path.join(save_directory, filename)
    
    # with open(filepath, 'w') as file:
    #     json.dump(data, file)

    # Save JSON string to a file
    save_directory = "services/epf-flower-data-science/src/data"
    os.makedirs(save_directory, exist_ok=True)

    filepath = os.path.join(save_directory, filename)

    with open(filepath, 'w') as file:
        file.write(data)