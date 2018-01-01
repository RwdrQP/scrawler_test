import re
import os
import os.path
import scrawler

#目录链接
def category_link(text):
    result = []
    matches = re.findall(r'<li>\s*<h2>Categories</h2>\s*<ul>\s*(<li.*</li>)\s*</ul>\s*</li>', text, re.DOTALL)
    print()
    if len(matches) == 0:
        return result
    text = matches[0]
    matches = re.findall(r'<a href="([^\"]*)"\s*>(\w+)</a>', text, re.DOTALL)
    for link in iter(matches):
        result.append(link)
    return result

#页面链接和下页链接
def getalllinks_sub(text):
    result = []
    matches = re.findall(r'\s+<h1 id="post-\d+">\s*<a href="([^<>\"]+)"', text, re.DOTALL)
    if len(matches) == 0:
        return result
    print('---')
    #当前页面的链接
    for link in iter(matches):
        result.append(link)
        print(link)

    #下页的链接
    matches = re.findall(r'<a href="([^<>]+)" >&laquo; Previous Entries', text, re.DOTALL)
    print(len(matches))
    if len(matches) > 0:
        nextresult = getalllinks(matches[0])
        result.extend(nextresult)
    return result

#目录下所有链接
def getalllinks(url):
    result = []
    req = scrawler.download(url)
    if req.status != scrawler.page.ERROR_OK:
        return result
    text = req.parse()
    ret = getalllinks_sub(text['body'])
    for link in iter(ret):
        result.append(link)
    return result

#下载网页
def downloadpage(url, dir, filename):
    req = scrawler.download(url)
    if req.status == scrawler.page.ERROR_OK:
        text = req.parse()
        matches = re.findall(r'\s+<h1 id="post-\d+">.*</h1>\s*<div class="entrytext">.*<!-- You can start editing here', text['body'], re.DOTALL)
        if len(matches) > 0:
            req.content = matches[0]
        scrawler.save(dir, filename, req, 'gbk')


def main():
    dict = {}
    req = scrawler.download(url = 'http://blog.farmostwood.net/')

    if req.status == scrawler.page.ERROR_OK:
        text = req.parse()
        result = category_link(text['body'])
        for link in iter(result):
            dict[link[1]] = getalllinks(link[0])

        print(dict)
        for v in iter(dict):
            print(v)
            print(dict[v])
            i = 1
            for v2 in iter(dict[v]):
                print(v2)
                path = os.path.join("F:/ptest", v)
                filename = str(i) + ".html"
                downloadpage(v2, path, filename)
                i = i + 1

#测试抓取某博主的所有blog
main()
