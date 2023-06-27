import json
import csv

def add_attributes_to_geojson(geojson_file, csv_file):
    with open(geojson_file, 'r') as file:
        geojson_data = json.load(file)
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)
    years = csv_data[0][1:]

    # Create a dictionary to store the frequency values for each ZIP code and year
    frequency_data = {}
    for row in csv_data[1:]:
        zipcode = row[0]
        frequencies = list(map(int, row[1:]))
        frequency_data[zipcode] = dict(zip(years, frequencies))

    # Iterate through the features in the GeoJSON and add attributes
    for feature in geojson_data['features']:
        zipcode = str(feature['properties']['ZCTA5CE10'])
        if zipcode in frequency_data:
            frequencies = frequency_data[zipcode]
            feature['properties'].update(frequencies)

    return geojson_data

def save_geojson(geojson_data, output_file):
    # Save the modified GeoJSON data to a file
    with open(output_file, 'w') as file:
        json.dump(geojson_data, file)

# Define the paths to the GeoJSON file and CSV file
geojson_file = 'pazipcodes.geojson'  # Replace with the actual path to your GeoJSON file
csv_file = '/users/miriamwaldvogel/Documents/Baker/Participant ZIP codes.csv'  # Replace with the actual path to your CSV file
output_file = 'Participant ZIP codes.geojson'  # Replace with the desired output file path

# Add attributes to the GeoJSON data
modified_geojson_data = add_attributes_to_geojson(geojson_file, csv_file)

# Save the modified GeoJSON data
save_geojson(modified_geojson_data, output_file)
