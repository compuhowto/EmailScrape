import urllib3, sys
import requests
import requests.exceptions
import argparse
import time
import re
from bs4 import BeautifulSoup
from urlparse import urlparse


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", help="host web address in http://www.site.com format", required=True)
	parser.add_argument("-f", "--efile", help="file name to store emails to", required=True)
	parser.add_argument("-l", "--lfile", help="file name to store links to", required=False)

	args = parser.parse_args()

	host = args.url
	outfi = args.efile
	lnkfi = args.lfile

	startparse(host,outfi,lnkfi)
	#print 'URL is - ', host
	#print 'Out file is -', outfi

def startparse(url,out,lnk):
	urls = [url]
	emails = []
	processed_urls = []

	while len(urls):
		parts = urlparse(urls[0])
		base_url = "{0.scheme}://{0.netloc}".format(parts)
		path = urls[0][:urls[0].rfind('/')+1] if '/' in parts.path else urls[0]

		processed_urls.append(urls[0])

		dt = time.strftime("%Y-%m-%d %H:%M")
		print '%s - %s' % (dt,urls[0])
		try:
			rsp = requests.get(urls[0],headers={'User-Agent':' Mozilla/5.0 (compatible; ebot/1.0;)'})
		except:
			pass

		#find all emails
		emls = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", rsp.text, re.I)
		if (len(emls) != 0):
			for n in emls:
				if (not n in emails):
					emails.append(n)
					fo = open(out, "a")
					fo.write(n + '\n')
					fo.close()
			emls = []

		
    		soup = BeautifulSoup(rsp.text)
    		for anchor in soup.find_all("a"):
			link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        		
        		if link.startswith('/'):
            			link = base_url + link
        		elif not link.startswith('http'):
            			link = path + link
        		
        		if (not link in urls) and (not link in processed_urls) and link.startswith(base_url):
            			urls.append(link)
				if lnk != '':
					fo = open(lnk, "a")
					fo.writelines(link+'\n')
					fo.close()
		
		urls.remove(urls[0])
		time.sleep(8)
	
	if len(emails) !=0:
		print str(len(emails)) + " - Emails found!"
	else:
		print "Sorry No Emails Found! :("

	if lnk != '':	
		print str(len(processed_urls)) + " - Links logged!"


	sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
