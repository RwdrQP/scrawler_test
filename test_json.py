import json

def load_data(path):
    data = None
    try:
        f = open(path, 'r')
        if f == None:
            pass
        else:
            try:
                data = json.load(f)
            except:
                pass
            finally:
                f.close()
    except:
        pass
    finally:
        return data

def dump_data(path, data):
    f = open(path, 'w')
    if f == None:
        return False
    else:
        try:
            json_str = json.dumps(data)
            f.write(json_str)
            f.flush()
        except:
            #todo:convert data to string
            pass
        finally:
            f.close()
        return True

def test_load():
    path = "page.json"
    data = load_data(path)
    if data == None:
        print("can not load json")
        return
    else:
        print("datatype: " + str(type(data)))
        url_file_dict = data['url_to_file']
        if url_file_dict == None or not isinstance(url_file_dict, dict):
            return
        else:
            print("url_to_file_type: " + str(type(url_file_dict)))
            it = iter(url_file_dict)
            for k in it:
                print(k + " : " + url_file_dict[k])


def test_dump():
    path = "page.json"
    data = {}
    data['url_to_file'] = {}
    data['url_to_file']['http://www.so.com'] = 'so.html'
    data['url_to_file']['http://www.sogou.com'] = 'sogou.html'
    if not dump_data(path, data):
        print("dump json fail")
    else:
        print("dump json ok")

test_load()
test_dump()
test_load()