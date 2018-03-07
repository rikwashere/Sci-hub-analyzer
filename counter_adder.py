from itertools import dropwhile
import matplotlib.pyplot as plt
from collections import Counter
import unicodecsv as csv
import time
import os

def write(counter, fo):
	with open(fo + '.csv', 'a') as csv_out:
		writer = csv.writer(csv_out, delimiter='\t')
		writer.writerows([c for c in counter.most_common(300000)])

counts = os.listdir('data')

doi_counter = Counter()
doi_c = 0
time_spent = []

for count in counts:
	if 'doi' in count:
		doi_c += 1
		t0 = time.time()
		print 'Processing %s.' % count

		with open('data/' + count) as csv_in:
			reader = csv.reader(csv_in, delimiter='\t')
			data = [[line[0], int(line[1])] for line in reader if int(line[1])]
			c = Counter(dict(data))
			doi_counter += c

		time_spent.append(time.time() - t0)

		if doi_c % 10 == 0:
			print 'Reducing Counter... Currently %i keys.' % len(doi_counter)

			for key, count in dropwhile(lambda key_count: key_count[1] > 1, doi_counter.most_common()):
				del doi_counter[key]

			print 'Counter reduced. %s keys currently.' % len(doi_counter)

		print 'Finished in: %.2f seconds.' % (time.time() - t0)

write(doi_counter, 'doi-fin')
