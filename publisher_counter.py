from collections import Counter
import unicodecsv as csv
import time
import sys

def process(chunk, counter):
	for line in chunk:
		doi = line[1]
		doi_prefix = doi.split('/')[0]

		if publisher.has_key(doi_prefix):
			counter[publisher[doi_prefix]] += 1
		else:
			counter['Unknown'] += 1

publisher = {}
counter = Counter()

with open('../data_processed/DOI/doi-prefixes.csv', 'r') as csv_in:
	reader = csv.reader(csv_in, delimiter='\t')

	for line in reader:
		doi_prefix = line[1].strip()
		publisher_str = line[0].strip()	

		publisher[doi_prefix] = publisher_str

with open('../data_raw/2017.statistics.tab', 'r') as csv_in:
	reader = csv.reader(csv_in, delimiter='\t')
	chunk = []

	for line in reader:
		t0 = time.time()
		chunk.append(line)

		if len(chunk) == 1000000:
			process(chunk, counter)

			chunk = []
			print 'Processing time: %.2f seconds.' % (time.time() - t0)
			print 'Counted %i individual publishers. %i dois analyzed.' % (len(counter), sum(counter.values()))

process(chunk, counter)

with open('Downloads-per-publisher.csv', 'a') as csv_out:
	writer = csv.writer(csv_out, delimiter='\t')
	writer.writerows(counter.items())