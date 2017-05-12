import requests
import json
import sys
import argparse
import os
import datetime
import fiss.firecloud.api as api

def build_filter_json(filter_attrs):
	filt = {
		"op":"and",
		"content":[]
	}

	for key in filter_attrs:
		search_attr = {
			"op":"in",
			"content":{
				"field":key,
				"value":filter_attrs[key]
			}
		}

		filt["content"].append(search_attr)

	return filt


def download_manifest(filt_json, is_legacy = False):
	
	#This is the API endpoint for performing a search on the GDC data portal and retrieving file information.
	files_endpt = 'https://api.gdc.cancer.gov/files'
	files_endpt_legacy = 'https://api.gdc.cancer.gov/legacy/files'

	#Creating a new name for the manifest file
	timestamp='{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
	manifest_filename="gdc_manifest_"+timestamp+".tsv"
	print("downloading manifest {0}".format(manifest_filename))

	params = {'filters':json.dumps(filt_json),'size':'30000','return_type':'manifest'}
	
	if is_legacy:
		# requests URL-encodes automatically
		response = requests.get(files_endpt_legacy, params = params)
	else:
		# requests URL-encodes automatically
		response = requests.get(files_endpt, params = params)

	#Writing the output to the manifest file
	with open(manifest_filename, 'wb') as handle:
		for block in response.iter_content(1024):
			handle.write(block)

	return manifest_filename

