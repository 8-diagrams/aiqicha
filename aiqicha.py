#!env python3

import time,datetime
import requests

import hashlib
import random



def build_headers(referer , ua):
    if not referer:
        referer = 'https://www.baidu.com'

    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept-Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Referer': referer,
               'User-Agent': ua}
    return headers

def get_req(fn, url, ua, referer, redirect, proxy=None):

    #url = "%E5%85%AC%E4%BC%97%E5%8F%B7%E8%BF%90%E8%90%A5"
    if proxy:
        resp = requests.get(url, headers= build_headers(referer,ua) , verify=False, timeout=8, allow_redirects=redirect, proxies=proxy)
    else:

        resp = requests.get(url, headers= build_headers(referer,ua) , verify=False, timeout=8, allow_redirects=redirect)

    return resp.text


def get_now():
    import datetime
    t = datetime.datetime.now()
    return t.strftime('%Y-%m-%d %H:%M:%S') 

def logfileHHH(strlog):
    f = open('./debug_51.log', 'a', encoding='utf8')
    f.write( get_now() + " " + strlog+"\n")
    f.close()

def parse_index(content):
    import json
    tag_2 = '/* eslint-enable */</script> <script type="text/javascript"'
    tag_1 = 'window.pageData ='
    idx_1 = content.find(tag_1)
    idx_2 = content.find(tag_2)
    logfileHHH ( "parse_index idx_s " + str(idx_1)  + " " + str(idx_2) )

    if (idx_2 > idx_1):

        mystr = content[idx_1 + len(tag_1) : idx_2].strip()
        len_str = len(mystr)
        if mystr[len_str-1]==';':
            mystr = mystr[0:len_str-1]
        j = json.loads(mystr)

        if len(j["result"]["resultList"]) > 0:
            item = j["result"]["resultList"][0]
            return item
        else :
            return None

    else :
        logfileHHH ( "CONTENT"  + content)
        return None

def get_item_name(item):
    import re
    entName = item['entName']
    pattern = re.compile(r'<[^>]+>',re.S)
    result = pattern.sub('', entName)
    return  item['pid'] , result


def access_pid(pid, url_prefix, ua):

    url = "https://aiqicha.baidu.com/detail/compinfo?pid=" + pid

    content = get_req('./company_tmp/' + pid + 'aiqi_detail.html', url, url_prefix, ua, True )
    
    return parse_detail(content)


def parse_detail(content):
    import json
    tag_2 = '/* eslint-enable */</script> <script type="text/javascript"'
    tag_1 = 'window.pageData ='
    idx_1 = content.find(tag_1)
    idx_2 = content.find(tag_2)
    logfileHHH ( "parse_detail idx_s " + str(idx_1)  + " " +  str(idx_2))


    if (idx_2 > idx_1):

        mystr = content[idx_1 + len(tag_1) : idx_2].strip()
        len_str = len(mystr)
        if mystr[len_str-1]==';':
            mystr = mystr[0:len_str-1]
        j = json.loads(mystr)

        return j["result"]
        

    else :
        return None

def get_company_info(name):

    import agent_dict
    ua = agent_dict.get_ua()

    company = name
 
    url_prefix = 'https://www.baidu.com/'
    #import load_city51
    url_a = 'https://aiqicha.baidu.com/s?q=' + company + '&t=0'
    
    content = get_req('./aiqi.html', url_a, url_prefix, ua, False )

    #print (content)
    item = parse_index(content)

    info = {}
    if item :
        my = get_item_name(item)
        #print (my[0], my[1])
        item_detail = access_pid(my[0], url_prefix, ua)

        info["telephone"] = item_detail["telephone"] 
        info["email"] = item_detail["email"] 
        info["website"] = item_detail["website"] 
        info["legalPerson"] = item_detail["legalPerson"]
        return info
    else:
        logfileHHH("parse_index none " + name)
        return "NO_INDEX"


if __name__ == '__main__':

    import sys
    
    company = sys.argv[1]
    info = get_company_info(company)

    print( "===") 

    info = get_company_info(company)


    print (info)


"""
   私域运营方案，访问 51dawo.com
"""
    