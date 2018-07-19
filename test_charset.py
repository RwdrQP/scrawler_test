import re

#replace charset notation in text
def repalce_charset_notation(content, new_notation):
#try:
    charset_re = re.compile(r'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I)
    pragma_re = re.compile(r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I)
    xml_re = re.compile(r'^<\?xml.*?encoding=["\']*(.+?)["\'>]')
    charset_all = charset_re.findall(content)
    pragma_all = pragma_re.findall(content)
    xml_all = xml_re.findall(content)
    def match_fun(orig):
        def match_func(match, origin = orig):
            newtext = re.sub(origin, new_notation, match.group(0))
            return newtext
        return match_func
    if charset_all:
        content = re.sub(r'<meta.*?charset=["\']*(.+?)["\'>]', match_fun(charset_all[0]), content)
    if pragma_all:
        content = re.sub(r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', match_fun(pragma_all[0]), content)
    if xml_all:
        content = re.sub(r'^<\?xml.*?encoding=["\']*(.+?)["\'>]', match_fun(xml_all[0]), content)
#except:
    #print("Exception in: repalce_charset_notation")
    return content



text = '<meta http-equiv="Content-Type" content="text/html; charset=gb2312">'
newtext = repalce_charset_notation(text, "utf-8")
print(text)
print(newtext)



