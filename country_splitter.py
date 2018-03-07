from prettytable import PrettyTable
from collections import Counter
from datetime import datetime
import unicodecsv as csv
import sqlite3
import time

chunk_size = 500000
country_count = Counter()
doi_count = Counter()
day_count = Counter()

def write(chunk):
	for row in chunk:
		# 2017-01-01 00:00:27    
		timestamp = row[0]
		timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
		date_str = timestamp.strftime('%Y-%m-%d')
		doi = row[1]
		country = row[4]
		row[0] = date_str

		row_out = row

		if country == 'N/A' or country == 'Netherlands':
			continue

		with open('data/countries/%s.csv' % country, 'a') as csv_out:
			writer = csv.writer(csv_out, delimiter='\t')
			writer.writerow(row_out)	

with open('data.tab', 'r') as fi:
	reader = csv.reader(fi, delimiter='\t')
	chunk = []
	chunk_c = 1
	t0 = time.time()

	for line in reader:
		chunk.append(line)

		if len(chunk) == chunk_size:

			print 'Chunk %i loaded.' % chunk_c

			print 'Writing...'
			write(chunk)
			print 'Done. Processing time: %.2f seconds.' % (time.time() - t0)
			chunk = []
			t0 = time.time()
			chunk_c += 1

write(chunk)