from urllib2 import Request, urlopen, URLError, HTTPError
from urllib import urlencode, quote
import simplejson as json
import re

GENERATOR='Xumblr 0.1'

def dashboard(email, password, num):
	url = 'http://www.tumblr.com/api/dashboard/json'
	
	values = {      
		'generator' : GENERATOR, 
        'email': email, 
        'password' : password,
        'type' : 'photo',
        'num' : num,
        'callback' : 'p'
    }
    
	data = urlencode(values)
	req = Request(url, data)

	try:
		response = urlopen(req)
		page = response.read()

		m = re.match("^.*?({.*}).*$", page,re.DOTALL | re.MULTILINE | re.UNICODE)
		results = json.loads(m.group(1))

		results_arr = []

		for p in results['posts']:
			results_arr.append(p['photo-url-1280'])

		return results
	except HTTPError, e:
		if 403 == e.code:
			raise TumblrAuthError(str(e))
		if 400 == e.code:
			raise TumblrRequestError(str(e))
	except Exception, e:
		print 'FUUUUUUUUUU'


if __name__ == "__main__":
    import sys
    print dashboard(int(sys.argv[1]))
