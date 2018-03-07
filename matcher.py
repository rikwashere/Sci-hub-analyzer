from crossref.restful import Works
import matplotlib.pyplot as plt
from collections import Counter
import unicodecsv as csv
import json
import time
import sys

data = []
doi_dict = {}

def add_to_doi_dict(doi_dict, doi_data):
	if not doi_dict.has_key(doi_data['DOI'].lower()):
		if doi_data.has_key('subject'):	
			doi_dict[doi_data['DOI'].lower()] = [su for su in doi_data['subject']]
		else:
			doi_dict[doi_data['DOI'].lower()] = [None]

	return doi_dict

print 'Building dictionaries...'
with open('../data_processed/DOI/DOI-WW-hydrated.json', 'r') as json_in:
	for line in json_in:
		doi_data = json.loads(line)
		add_to_doi_dict(doi_dict, doi_data)

with open('../data_processed/DOI/DOI-NL-hydrated.json', 'r') as json_in:
	for line in json_in:
		doi_data = json.loads(line)
		add_to_doi_dict(doi_dict, doi_data)

print 'Loaded %i DOI in dictionary' % len(doi_dict)

subject_count = Counter()
t0 = time.time()

with open('../data_processed/DOI-all.csv', 'r') as csv_in:
	reader = csv.reader(csv_in, delimiter='\t')

	for doi, count in reader:
		print 'Looking up DOI <%s>. Downloaded %i times...' % (doi, int(count))
		doi = doi.lower()
		if doi_dict.has_key(doi):
			if doi_dict[doi] != None:
				print '\tMatched locally. Found %i subjects.' % (len(doi_dict[doi]))
				subjects =doi_dict[doi]
			else:
				print '\tMatched locally. But no subject data available at CrossRef.'
		else:
			print '\tNo local match. Crawling...'
			
			nap_time = (time.time() - t0) * 10
			print '\t\tSleeping for %.2f seconds.' % nap_time
			time.sleep(nap_time)

			t0 = time.time()
			works = Works()
			results = works.doi(doi)

			if results:
				print '\tFound results...'
				doi_dict = add_to_doi_dict(doi_dict, results)
				print '\tMatched online. Found %i subjects.' % (len(doi_dict[doi]))
				subjects = doi_dict[doi]

				# add to data_file
				with open('../data_processed/DOIs-WW-hydrated.json', 'a') as json_out:
					json.dump(results, json_out)
					json_out.write('\n')
			else:
				print '\tNo CrossRef data for DOI <%s>.' % (doi)
				subjects = [ None ]