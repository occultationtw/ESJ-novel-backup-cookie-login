#!/usr/bin/env python
#coding=utf-8

import requests
import lxml.html
import re
import json
import os
import sys

from lxml import etree

symbol_list = {
    "\\": "-",
    "/": "-",
    ":": "：",
    "*": "☆",
    "?": "？",
    "\"": " ",
    "<": "《",
    ">": "》",
    "|": "-",
    ".": "。",
    "\t": " ",
    "\n": " ",
}

def get_with_cookies(url, cookie_file='cookie.txt'):
    # Load cookies from the file
    with open(cookie_file, 'r', encoding='utf-8') as file:
        cookies = json.load(file)

    # Create a session object
    session = requests.Session()

    # Add each cookie to the session
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])

    # Make a GET request with the cookies
    response = session.get(url)

    return response

def write_page(url, dst_file, single_file=True):
    r = get_with_cookies(url)
    html_element = lxml.html.document_fromstring(r.text)
    if html_element.xpath('//h2'):
        title = html_element.xpath('//h2')[0]
        author = html_element.xpath('//div[@class="single-post-meta m-t-20"]/div')[0]
        content = html_element.xpath('//div[@class="forum-content mt-3"]')[0]
        if single_file:
            with open(dst_file, 'a', encoding='utf-8') as f:
                f.write('[' + title.text_content() + '] ' + author.text_content().strip() + '\n')
                f.write(content.text_content()+'\n\n')
        else:
            with open(dst_file, 'w', encoding='utf-8') as f:
                f.write('[' + title.text_content() + '] ' + author.text_content().strip() + '\n')
                f.write(content.text_content()+'\n\n')

def contain(string: str, array):
    if isinstance(array, dict):
        return any(symbol in string for symbol in array.keys())
    elif isinstance(array, list) or isinstance(array, tuple):
        return any(symbol in string for symbol in array)
    return False


def escape_symbol(string: str):
    while contain(string, symbol_list):
        for char, replace_char in symbol_list.items():
            string = string.replace(char, replace_char)
    return string


if __name__ == "__main__":

    current_path = os.path.split(os.path.realpath(__file__))[0]
    novel_flag = False
    forum_flag = False
    page_flag = False

    if len(sys.argv) == 1:
        print("Usage: ", __file__, " https://www.esjzone.cc/detail/1599746513.html")
        print("       ", __file__, " https://www.esjzone.cc/forum/1584679807/1599746513/")
        print("       ", __file__, " https://www.esjzone.cc/forum/1599746513/121688.html")
        sys.exit()
    
  
    url = sys.argv[1]
    if re.search(r'https://www\.esjzone\.cc/detail/\d+\.html', url):
        novel_flag = True
    elif re.search(r'https://www\.esjzone\.cc/forum/\d+/\d+/', url):
        forum_flag = True
    elif re.search(r'https://www\.esjzone\.cc/forum/\d+/\d+\.html', url):
        page_flag = True
    else:
        print("Wrong url")
        sys.exit()


    if novel_flag :
        r = get_with_cookies(url)
        html_element = lxml.html.document_fromstring(r.text)
        
        '''測試網站內容用
        html_content = etree.tostring(html_element, pretty_print=True, method="html")
        html_string = html_content.decode("utf-8")
        with open('test.txt', 'a', encoding='utf-8') as f:
            f.write(html_string)
        '''
        
        #抓取書名
        novel_name = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content()
        novel_name = escape_symbol(novel_name)
        print('='*50)
        print(f'小說名稱：{novel_name}')
        dst_filename = os.path.normpath( current_path + '/' + novel_name + '.txt')
        with open(dst_filename, 'w', encoding='utf-8') as f:
            f.write(u"書名: " + novel_name + "\n")
        with open(dst_filename, 'a', encoding='utf-8') as f:
            f.write(u"URL: " + url)

        #抓取小說細節說明
        novel_details_element = html_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]')[0]
        if novel_details_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]/li/div'):
            bad_divs = novel_details_element.xpath('//ul[@class="list-unstyled mb-2 book-detail"]/li/div')
            for bad_div in bad_divs:
                bad_div.getparent().remove(bad_div)
        novel_details = novel_details_element.text_content()
        print('='*50)
        print(f'小說細節：\n{novel_details}')
        with open(dst_filename, 'a', encoding='utf-8') as f:
            f.write(novel_details)

        #抓取外部連結
        novel_outlink_element = html_element.xpath('//div[@class="row out-link"]')[0]
        if len(novel_outlink_element) != 0:
            outlink_list = novel_outlink_element.getchildren()
            for element in outlink_list:
                with open(dst_filename, 'a', encoding='utf-8') as f:
                    f.write(element.getchildren()[0].text_content() + u":\n" + element.getchildren()[0].attrib['href'] + "\n")

        if re.search('id="details"', r.text):
            novel_description = html_element.get_element_by_id("details").text_content()
            print('='*50)
            print(f'小說介紹：{novel_description}')
            with open(dst_filename, 'a', encoding='utf-8') as f:
                f.write(novel_description)
        else:
            with open(dst_filename, 'a', encoding='utf-8') as f:
                f.write('\n\n')

        #抓取小說章節區塊
        if re.search('id="chapterList"', r.text):
            #章節區塊元素的子節點
            chapter_list = html_element.get_element_by_id("chapterList").getchildren()
            
            #抓沒展開的章節         
            for element in chapter_list:
                if element.tag == 'details':
                    chapter_list_b = element.getchildren()
                    for element_b in chapter_list_b:
                        print('-'*50)
                        print('正在獲取內容')
                        print(f'本話標題：{element_b.text_content()}')

                        with open(dst_filename, 'a', encoding='utf-8') as f:
                            f.write(element_b.text_content()+'\n')
                        
                        if element_b.tag == 'a':
                            if re.search(r'esjzone\.cc/forum/\d+/\d+\.html', element_b.attrib['href']):
                                write_page(element_b.attrib['href'], dst_filename, single_file=True)
                                print(f'本話內文：{element_b.attrib["href"]}')
                            else:
                                with open(dst_filename, 'a', encoding='utf-8') as f:
                                    f.write(element_b.attrib['href'] + u' {非站內連結，略過}\n\n')
            
            #抓原本就展開的章節
            for element in chapter_list:
                if element.tag != 'details':
                    print('-'*50)
                    print('正在獲取內容')
                    print(f'本話標題：{element.text_content()}')

                    with open(dst_filename, 'a', encoding='utf-8') as f:
                        f.write(element.text_content()+'\n')
                    
                    if element.tag == 'a':
                        if re.search(r'esjzone\.cc/forum/\d+/\d+\.html', element.attrib['href']):
                            write_page(element.attrib['href'], dst_filename, single_file=True)
                            print(f'本話內文：{element.attrib["href"]}')
                        else:
                            with open(dst_filename, 'a', encoding='utf-8') as f:
                                f.write(element.attrib['href'] + u' {非站內連結，略過}\n\n')
    

    if forum_flag:
        r = get_with_cookies(url)
        html_element = lxml.html.document_fromstring(r.text)
        novel_name = html_element.xpath('//h2[@class="p-t-10 text-normal"]')[0].text_content()
        novel_name = escape_symbol(novel_name)

        m = re.search(r"var mem_id='(u?\d+)',mem_nickname='.*',token='(.+)';", r.text) 
        mem_id, token = m.groups()
        m = re.search(r"forum_list_data\.php\?token=.+&totalRows=(\d+)&bid=(\d+)", r.text) 
        totalRows, bid = m.groups()

        r = get_with_cookies(url + 'forum_list_data.php?token=' + token + '&totalRows=' + str(totalRows) + '&bid=' + str(bid) + \
                         '&sort=cdate&order=asc&offset=0&limit=' + str(totalRows))

        chapter_josn = json.loads(r.text)

        if chapter_josn["rows"]:

            if not os.path.isdir( os.path.normpath( current_path + '/' + novel_name ) ):
                os.system("mkdir " + str(os.path.normpath( current_path + '/' + novel_name )))

            for chapter in chapter_josn["rows"]:
                chapter_name = chapter["subject"].split('target="_blank">')[1].split('</a>')[0]
                chapter_name = escape_symbol(chapter_name)
                dst_filename = os.path.normpath( current_path + '/' + novel_name + '/' + chapter_name + '.txt')
                chapter_url = re.sub(r'/forum/\d+/\d+/', chapter["subject"].split('"')[1], url)
                write_page(chapter_url, dst_filename, single_file=False)


    if page_flag :
        write_page(url, url.split('/')[-1].split('.')[0] + ".txt", single_file=False)
