import csv
with open('CSV/SA01552.csv') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        print(row['Date'], row['Time'], row['CASSERO'], row['TRAVERSA'].lstrip(), row['MIN'].lstrip(), row['MAX'])