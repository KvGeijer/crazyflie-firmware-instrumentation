import cfusdlog
import matplotlib.pyplot as plt
import re
import argparse
import os
import json

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
name = args.filename[-5:]


# decode binary log data
logData = cfusdlog.decode(args.filename)


if not os.path.isdir('decoded'):
	os.mkdir('decoded')

with open(os.path.join('decoded',name + '.json'), 'w') as f:
	# print(logData)
	json.dump(logData, f, indent=4)
		



