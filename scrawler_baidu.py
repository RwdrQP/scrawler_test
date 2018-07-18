import scrawler

def main():
	url = "http://www.baidu.com/"
	print("downloading " + url)
	html = scrawler.download(url)
	if html.status == scrawler.page.ERROR_EXCEPT:
		print("exception")
	elif html.status == scrawler.page.ERROR_INPUT:
		print("input none")
	elif html.status == scrawler.page.ERROR_SERVER:
		print("server error")
	elif html.status == scrawler.page.ERROR_OTHER:
		print("other error")
	elif html.status == scrawler.page.ERROR_OK:
		print("ok")
		#print(html.content)
		scrawler.save("/home/anonymous/webscrawler", "baidu.html", html)

main()
