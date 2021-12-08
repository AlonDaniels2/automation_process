import pandas as pd
import glob
import os
import log_funcs
import sys

def handle_csv_file():
    """Open last downloaded csv file with pandas. Handle it and re-save it to \\Downloads.
    """

    # Find last csv file in \\Downloads.
    try:
        folder_path = r'F:\Downloads'
        file_type = '\*csv'
        files = glob.glob(folder_path + file_type)
        filename = max(files, key=os.path.getctime)
    except Exception as e:
        log_funcs.log_error(e)
        sys.exit()

    try:
        # Store a pandas copy to data.
        data = pd.read_csv(filename).copy()

        # Fetch addresses from data and store into addresses list as uppercase.
        addresses = data['Address']
        addresses = list(addresses)
        for i in range(len(addresses)):
            addresses[i] = str(addresses[i]).upper()

        # Drop irrelevant columns.
        data = data.drop(
            ['Address', 'Record Number', 'Date', 'Record Type', 'Short Notes', 'Status', data.columns[-1]], axis=1)

        # Split into "address" and "city state zipcode"
        splitted = [list((address.split(', ')[0], address.split(', ')[-1])) for address in addresses]

        # Using split fetch relevant address, city, state and zipcode
        address_column = [s[0] for s in splitted]
        city_column = [s[1].split(' KY ')[0] for s in splitted]
        state_column = [s[1].split()[len(s[1].split()) - 2] for s in splitted]
        zipcode_column = [s[1].split()[-1] for s in splitted]

        # Create new columns for these entries.
        data['address'] = address_column
        data['city'] = city_column
        data['state'] = state_column
        data['zipcode'] = zipcode_column

        # Drop all rows with problematic zipcodes
        bad_zipcodes = ['40202', '40203', '40210', '40211', '40212']
        for index, row in data.iterrows():
            if row['zipcode'] in bad_zipcodes or not row['zipcode'].isnumeric():
                data = data.drop(index, axis=0)

    # If any exception is raised
    except Exception as e:
        log_funcs.log_error(e)
    else:
        # Create new csv file in \\Downloads.
        data.to_csv(filename, index=False)