#!/usr/bin/env python3
import sys

def reduce_count():
	current_key = None
	current_count = 0

	for line in sys.stdin:
		line = line.strip()
		if not line:
			continue

		if '\t' not in line:
			continue

		try:
			key, count = line.split('\t', 1)
			count = int(count)
		except (ValueError, IndexError):
			continue
		
		if current_key == key:
			current_count += count
		else:
			if current_key:
				print(f"{current_key}\t{current_count}")
			current_key = key
			current_count = count
	if current_key:
		print(f"{current_key}\t{current_count}")

if __name__ == "__main__":
	reduce_count()
