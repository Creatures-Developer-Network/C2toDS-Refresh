# Some quick code to convert the C2toDS Classifiers.csv into catalogue format.
import csv

with open('c2tods_refresh.catalogue', 'w') as f:
	with open('C2toDS Classifiers.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
			else:
				f.write(f'TAG \"Agent Help {row[1]} {row[2]} {row[3]}\"\n\"{row[6]}\"\n\"{row[7]} \"\n\n')
				line_count += 1
		print(f'Processed {line_count} lines.')
    
    