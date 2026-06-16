#!usr/bin/env python3
import sys
import json
import re

sentiment_dict = {}
try:
	with open('sentiment_dict.txt', 'r', encoding='utf-8') as f:
		for line in f:
			line = line.strip()
			if not line:
				continue
			parts = line.split()
			if len(parts) >= 2:
				score = parts[-1]
				word = " ".join(parts[:-1]).lower()
				try:
					sentiment_dict[word] = int(score)
				except:
					continue
except:
	pass

for line in sys.stdin:
	line = line.strip()
	if not line:
		continue
	try:
		data = json.loads(line)
		content = data.get('content', '')
		if not content or not isinstance(content, str):
			continue
		url = data.get('url', '')
		source_type = "VN" if (".vn" in url or "dantri" in url or "vnexpress" in url) else "Global"
		content = re.sub('[^\\w\\s]', ' ', content).lower()
		words = content.split()
		score = 0
		for word in words:
			if word in sentiment_dict:
				score += sentiment_dict[word]
		if score > 0:
			sentiment = "Positive"
		elif score < 0:
			sentiment = "Negative"
		else: 
			sentiment = "Neutral"

		print(f"{source_type}\t{sentiment}\t1")
	except:
		continue
