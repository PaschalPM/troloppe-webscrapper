import csv

def convert_to_csv(data: list, filename = 'output.csv'):

    # Writing to CSV file
    with open(f"storage/csv/{filename}", mode='w', newline='', encoding='utf-8') as file:
        # Extract the fieldnames from the first dictionary
        fieldnames = data[0].keys()
        
        # Create a DictWriter object
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the rows
        writer.writerows(data)

    print("CSV file created successfully.")
