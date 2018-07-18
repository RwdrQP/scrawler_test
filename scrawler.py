#Date: 2017.12.30
#Writen By: QuanLongJie
#Function: download web pages
import re
import os
import requests

class page:
    ERROR_OK = 0
    ERROR_INPUT = 1
    ERROR_SERVER = 2
    ERROR_EXCEPT = 3
    ERROR_OTHER = 4
    def __init__(self, url, content, status_code):
        self.url = url
        self.content = content
        self.status  = status_code

    #parse pagecontent into title, head and body
    def parse(self):
        content = {'title' : '', 'head' : '', 'body' : ''}
        matchs = re.findall(r'<head.*</head>', self.content, re.DOTALL)
        if matchs[0] != None:
            content['head'] = matchs[0]
        matchs = re.findall(r'<title.*</title>', content['head'], re.DOTALL)
        if matchs[0] != None:
            content['title'] = matchs[0]
        matchs = re.findall(r'<body.*</body>', self.content, re.DOTALL)
        if matchs[0] != None:
            content['body'] = matchs[0]
        return content

#replace charset notation in text
def replace_charset_notation(content, new_notation):
    charset_re = re.compile(r'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I)
    pragma_re = re.compile(r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I)
    xml_re = re.compile(r'^<\?xml.*?encoding=["\']*(.+?)["\'>]')
    charset_all = charset_re.findall(content)
    pragma_all = pragma_re.findall(content)
    xml_all = xml_re.findall(content)
    #replace function
    def match_fun(origin):
        def match_fun_real(match, old_notation = origin):
            newtext = re.sub(old_notation, new_notation, match.group(0))
            return newtext
        return match_fun_real

    if charset_all:
        content = re.sub(r'<meta.*?charset=["\']*(.+?)["\'>]', match_fun(charset_all[0]), content)
    if pragma_all:
        content = re.sub(r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', match_fun(pragma_all[0]), content)
    if xml_all:
        content = re.sub(r'^<\?xml.*?encoding=["\']*(.+?)["\'>]', match_fun(xml_all[0]), content)
    return content

#download page,response only parse to text
#todo:able to parse bytes content(like jpg) 
def download(url, retry_times = 2):
    if url == None:
        return page(url, "", 1)
    try:
        response = requests.get(url)
        #print("status_code: " + response.status_code)
        if response.status_code == 200:
            #requests lib default encoding is not utf-8,try to get charset from response
            encodings = requests.utils.get_encodings_from_content(response.text)
            if encodings:
                #print("coding: " + encodings[0])
                response.encoding = encodings[0]
            else:
                response.encoding = 'utf-8'
            return page(url, response.text, 0)
        if 500 <= response.status_code < 600:
            if retry_times == 0:
                return page(url, "", 2)
            else:
                return download(url, retry_times - 1)
    except:
        return page(url, "", 3)
    return page(url, "", 4)

#save page
def save(dir, filename, page, encoding = 'utf-8', errors = 'ignore'):
    path = os.path.join(dir, filename)
    print(path)
    if os.path.exists(path):
        print('path exist')
        return
    else:
        print("not exit")
        if not os.path.exists(dir):
            os.makedirs(dir)
        file = open(path, 'wb')
        if file == None:
            return
        #default ignore wrong string
        page.content = replace_charset_notation(page.content, encoding)
        content = page.content.encode(encoding, errors)
        file.write(content)
        file.flush()
        file.close()





######below are test codes######
#html = download("http://www.baidu.com")
#if html.status == page.ERROR_EXCEPT:
#    print("exception")
#elif html.status == page.ERROR_INPUT:
#    print("input none")
#elif html.status == page.ERROR_SERVER:
#    print("server error")
#elif html.status == page.ERROR_OTHER:
#    print("other error")
#elif html.status == page.ERROR_OK:
#    print("ok")


