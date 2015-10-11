class KoboFirmware:
	
	def reset(self):
		
		self.upgrade = None
		self.releaseNote = None
	
	def __init__(self, eReader, affiliate):
		
		self.reset()
		try:
			from urllib import urlopen
			response = urlopen('https://api.kobobooks.com/1.0/UpgradeCheck/Device/' + eReader + '/' + affiliate + '/0.0.0/dummy')
			import json
			firmware = json.load(response)
			from urlparse import urlparse
			self.upgrade = firmware['UpgradeURL']
			url = urlparse(self.upgrade)
			if (url.scheme != 'http') and (url.scheme != 'https'):
				self.upgrade = None
			self.releaseNote = firmware['ReleaseNoteURL']
			url = urlparse(self.releaseNote)
			if (url.scheme != 'http') and (url.scheme != 'https'):
				self.releaseNote = None
		except:
			self.reset()

def app(environ, start_response):
	
	body = """<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
<title>Kobo firmware check</title>
<link rel="icon" type="image/png" href="https://assets.kobo.com/skin/frontend/enterprise/kobo/favicon.ico">
<script type=\"text/javascript\">
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-55369806-2', 'auto');
  ga('send', 'pageview');

</script>
<style media=\"screen\" type=\"text/css\">
* {
	font-family: Arial, Helvetica, sans-serif;
	text-decoration: none;
}

body {
	margin-top: 2.5%;
	margin-bottom: 2.5%;
	margin-left: 12.5%;
	margin-right: 12.5%;
	font-size: 12pt;
	text-align: center;
}

h1 {
	font-size: 200%;
	font-weight: normal;
	margin-top: 1em;
	margin-bottom: 1em;
}

h2 {
	font-size: 150%;
	font-weight: normal;
	margin-top: 1em;
	margin-bottom: 1em;
}

p {
	margin-top: 1em;
	margin-bottom: 1em;
}

p.footer {
	margin-top: 3em;
	margin-bottom: 3em;
}

p.copyright {
	margin-top: 6em;
	font-size: 75%;
}

ul {
	margin-top: 1em;
	margin-left: 12.5%;
	margin-right: 12.5%;
	margin-bottom: 1em;
	text-align: left;
}

select {
	width: 37.5%;
}
</style>
</head>
<body>
"""
	
	body += """<h1>Is your Kobo eReader up-to-date?</h1>\n"""
	
	if environ['PATH_INFO'] == '/check':
		
		# check route
		
		from cgi import parse_qs, escape
		parameters = parse_qs(environ['QUERY_STRING'])
		eReader = escape(parameters.get('ereader', [''])[0])
		affiliate = escape(parameters.get('affiliate', [''])[0])
		
		t = KoboFirmware(eReader, affiliate)
		
		try:
			body += """<h2>Kobo firmware</h2>"""
			body += """<p>Manual updates are easy to perform, but please read <a href=\"""" + escape(t.releaseNote.encode('utf-8')) + """\">release notes</a> first!</p>\n"""
			body += """<ul><li>Download <a href=\"""" + escape(t.upgrade.encode('utf-8')) + """\">this</a> file.</li>"""
			body += """<li>Unpack the <em>.zip</em> file you just downloaded.</li>"""
			body += """<li>Attach your eReader to a computer.</li>"""
			body += """<li>Place the resulting files and directories in the <em>.kobo</em> folder of your eReader.</li>"""
			body += """<li>Safely remove (&quot;eject&quot;) your eReader and wait for the update to finish.</li></ul>\n"""
			body += """<p>Please also note that the firmware file has been directly provided by Kobo - I do not host any downloads!</p>\n"""
		except:
			body += """<h2>No firmware file is available at this time.</h2>\n"""
			body += """<p>There's nothing I can do about it, please try again later.</p>\n"""
		
		body += """<p class=\"footer\"><a href=\"/\">Go back to the product selection page</a></p>\n"""
		
		# end check route
		
	else:
		
		# default route
		
		body += """<h2>Download firmware directly from Kobo</h2>\n"""
		body += """<p>Please note that the links below have been directly provided by Kobo - I do not host any firmware downloads!</p>\n"""
		
		affiliates = [
			['Kobo', 'kobo'],
			['Beta', 'beta'],
			['Best Buy Canada', 'bestbuyca']
		]
		
		eReaders = [
			['Kobo Touch', '00000000-0000-0000-0000-000000000310'],
			['Kobo Touch 2.0', '00000000-0000-0000-0000-000000000320'],
			['Kobo Glo', '00000000-0000-0000-0000-000000000330'],
			['Kobo Mini', '00000000-0000-0000-0000-000000000340'],
			['Kobo Aura HD', '00000000-0000-0000-0000-000000000350'],
			['Kobo Aura/Aura H20', '00000000-0000-0000-0000-000000000360'],
			['Kobo Glo HD', '00000000-0000-0000-0000-000000000370']
		]
		
		body += """<p>Queries data feed which eReaders use.</p>\n"""
		
		body += """<form action=\"/check\" method=\"get\">"""
		body += """<p><select name=\"ereader\"><optgroup label=\"ereader\">"""
		for i in eReaders:
			if len(i[1]) > 0:
				body += """<option value=\"""" + i[1] + """\">""" + i[0] + """</option>"""
		body += """</optgroup></select></p>\n"""
		
		body += """<p><select name=\"affiliate\"><optgroup label=\"affiliate\">"""
		for i in affiliates:
			if len(i[1]) > 0:
				body += """<option value=\"""" + i[1] + """\">""" + i[0] + """</option>"""
		body += """</optgroup></select></p>\n"""
		body += """<p><input type=\"submit\" value=\"Check\"></p></form>\n"""
		
		# end default route
		
	body += """<p class=\"copyright\">Copyright &copy; 2015 by <a href=\"http://www.mobileread.com/forums/member.php?u=233967\">vatazhka</a> &reg;</p>\n"""
	body += """</body>
</html>"""
	
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(body)))])
	return [body]
