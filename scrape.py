import re
import requests
from bs4 import BeautifulSoup
import csv

s = requests.Session()
main_res  = s.get("https://www.dawn.com/elections/blog/")
main = BeautifulSoup(main_res.text, "lxml")

with open('main.html', 'w') as f:
    f.write(main_res.text.encode('utf-8'))

#print(re.match("story__content    text--400      story__content--normal", main_res.text))

articles = main.find_all("h2", {"data-layout":"story", "class":re.compile("story__title")})
dat = {}
for article in reversed(articles):
    did = article['data-id']
    name = re.findall('[NAPFBKS]{2}\-[0-9]*', article.text)
    if len(name):
        nm = name[0][0:2] + name[0][3:].zfill(3)
    else:
        continue
    story = article.parent.find_next("div").find_next("div")
    story_text = '\n'.join([t.text for t in story.find_all("p")])
    if len(re.findall("Unofficial\, preliminary results", story_text)):
        print nm
        print "here"
        print story_text
        ps_match = re.search("preliminary results from\: ([0-9\/]*)", story_text).group(1)
        
        name_matches = re.findall(".*\([A-Za-z\- ]*\).*[votes0-9\,]*", story_text)
        print name_matches
    else:
        continue
    dat[nm] = [name[0]] + name_matches + [ps_match]

with open("dawn_unofficial.csv",'wb') as of:
    wr = csv.writer(of)
    for key in sorted(dat):
        wr.writerow(dat[key])
