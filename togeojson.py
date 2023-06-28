import json
import csv

def add_attributes_to_geojson(geojson_file, csv_file):
    with open(geojson_file, 'r') as file:
        geojson_data = json.load(file)
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)
    years = csv_data[0][1:]
    emptyzipdict = {}
    for year in years:
        emptyzipdict[year] = 0;
    frequency_data = {}
    for row in csv_data[1:]:
        zipcode = row[0]
        frequencies = list(map(int, row[1:]))
        frequency_data[zipcode] = dict(zip(years, frequencies))

    for feature in geojson_data['features']:
        zipcode = str(feature['properties']['ZCTA5CE10'])
        if zipcode in frequency_data:
            frequencies = frequency_data[zipcode]
            feature['properties'].update(frequencies)
        else:
            feature['properties'].update(emptyzipdict)

    return geojson_data

def save_geojson(geojson_data, output_file):
    with open(output_file, 'w') as file:
        json.dump(geojson_data, file)

geojson_file = 'pazipcodes.geojson'
csv_file = '/users/miriamwaldvogel/Documents/Baker/Participant ZIP codes.csv'
output_file = 'Participant ZIP codes.geojson'

modified_geojson_data = add_attributes_to_geojson(geojson_file, csv_file)

save_geojson(modified_geojson_data, output_file)
