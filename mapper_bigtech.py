import sys
import json
import string

def clean_and_map():
	tech_companies = {'apple': 'Apple', 'google': 'Google', 'microsoft': 'Microsoft', 'samsumg': 'Samsung', 'nvidia': 'Nvidia', 'openai': 'OpenAI', 'vinfast': 'VinFast'}
	for line in sys.stdin:
		line = line.strip()
		if not line:
			continue
		line_lower = line.lower()

		source = 'VN' if '.vn' in line_lower or 'chủ đề' in line_lower else 'Global'
		
		for company_key, company_name in tech_companies.items():
			if company_key in line_lower:
				count = line_lower.count(company_key)
				for _ in range(count):
					print(f"{source}_{company_name}\t1")

if __name__ == "__main__":
	clean_and_map()
