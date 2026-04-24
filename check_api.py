import urllib.request
import json

url = "https://orr-backend.orr.solutions/admin-portal/v1/cms/all-content/?lang=it"
req = urllib.request.Request(url)
response = urllib.request.urlopen(req)
data = json.loads(response.read().decode('utf-8'))

for faq in data['data']['faqs']:
    print("Question:", faq['question'])
