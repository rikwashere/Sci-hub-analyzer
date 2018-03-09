from crossref.restful import Works
import matplotlib.pyplot as plt
from collections import Counter
import unicodecsv as csv
import json
import time
import sys
import os

data = []
doi_dict = {}

def add_to_doi_dict(doi_dict, doi_data):
	if not doi_dict.has_key(doi_data['DOI'].lower()):
		if doi_data.has_key('subject'):	
			doi_dict[doi_data['DOI'].lower()] = [su for su in doi_data['subject']]
		else:
			doi_dict[doi_data['DOI'].lower()] = [None]

	return doi_dict

def count_dois(fo_str):
	print 'Counting DOIs for <%s>.' % fo_str
	with open('../data_processed/countries/%s' % fo_str, 'r') as fo:
		reader = csv.reader(fo, delimiter='\t')
		return Counter([line[1].lower() for line in reader])

print 'Building dictionaries...'
with open('../data_processed/DOI/DOI-WW-hydrated.json', 'r') as json_in:
	for line in json_in:
		try:
			doi_data = json.loads(line)
		except ValueError:
			continue
		add_to_doi_dict(doi_dict, doi_data)

with open('../data_processed/DOI/DOI-NL-hydrated.json', 'r') as json_in:
	for line in json_in:
		doi_data = json.loads(line)
		add_to_doi_dict(doi_dict, doi_data)

print 'Loaded %i DOI in dictionary.' % len(doi_dict)

t0 = time.time()
fo_str = 'Netherlands.csv'

with open('../data_processed/countries/%s' % fo_str, 'r') as fo:
	print 'Reading data from <%s>.' % fo
	doi_counter = count_dois(fo_str)
	print 'Read %i DOI from <%s>. %i unique.' % (sum(doi_counter.values()), fo, len(doi_counter))
	
	for doi, count in doi_counter.most_common():
		if count > 1:
			print 'Looking up DOI <%s>. %i downloads...' % (doi, count)
			if doi_dict.has_key(doi):
				if doi_dict[doi] != [ None ]:
					print '\tMatched locally. Found %i subjects.' % (len(doi_dict[doi]))
					subjects = doi_dict[doi]
				else:
					print '\tMatched locally. But no subject data available at CrossRef.'
					subjects = [None]
			else:
				print '\tNo local match. Crawling...'
				
				nap_time = (time.time() - t0) * 10
				print '\t\tSleeping for %.2f seconds.' % nap_time
				time.sleep(nap_time)
				t0 = time.time()
				works = Works()
				results = works.doi(doi)

				if results:
					doi_dict = add_to_doi_dict(doi_dict, results)
					print '\tMatched online.'
					subjects = doi_dict[doi]
					if doi_dict[doi] != [ None ]:
						print '\tFound %i subjects.' % len(doi_dict[doi])
					else:
						print '\tNo subject data availble at CrossRef.'
					# add to data_file
					with open('../data_processed/DOI/DOI-WW-hydrated.json', 'a') as json_out:
						json.dump(results, json_out)
						json_out.write('\n')
				else:
					print '\tNo CrossRef data for DOI <%s>.' % (doi)
					subjects = [ None ]

			with open('../data_processed/subject/%s' % 'Netherlands.csv', 'a') as csv_out:
				writer = csv.writer(csv_out, delimiter='\t')
				row = [doi, count] + subjects
				writer.writerow(row)
