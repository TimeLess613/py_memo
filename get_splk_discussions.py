import requests
import re
import time

target_1001 = re.compile('.*exam-splk-1001-topic-1-question.*')
target_1002 = re.compile('.*exam-splk-1002-topic-1-question.*')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

for i in range(1,47):
    # if i > 1: break
    # url = f'https://www.examtopics.com/discussions/splunk/1/'
    print(f"### {i}")
    url = f'https://www.examtopics.com/discussions/splunk/{i}/'
    rep = requests.get(url, headers=headers)
    search_target = target_1002.findall(rep.text)
    if search_target:
        [print("https://www.examtopics.com"+_.strip().split('"')[1]) for _ in search_target]
    time.sleep(2)
