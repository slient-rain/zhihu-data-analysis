# -*- coding: utf-8 -*-
'''

                                                                                         ;$$;
                                                                                    #############
                                                                               #############;#####o
                                                      ##                 o#########################
                                                      #####         $###############################
                                                      ##  ###$ ######!    ##########################
                           ##                        ###    $###          ################### ######
                           ###                      ###                   ##o#######################
                          ######                  ;###                    #### #####################
                          ##  ###             ######                       ######&&################
                          ##    ###      ######                            ## ############ #######
                         o##      ########                                  ## ##################
                         ##o                ###                             #### #######o#######
                         ##               ######                             ###########&#####
                         ##                ####                               #############!
                        ###                                                     #########
               #####&   ##                                                      o####
             ######     ##                                                   ####*
                  ##   !##                                               #####
                   ##  ##*                                            ####; ##
                    #####                                          #####o   #####
                     ####                                        ### ###   $###o
                      ###                                            ## ####! $###
                      ##                                            #####
                      ##                                            ##
                     ;##                                           ###                           ;
                     ##$                                           ##
                #######                                            ##
            #####   &##                                            ##
          ###       ###                                           ###
         ###      ###                                             ##
         ##     ;##                                               ##
         ##    ###                                                ##
          ### ###                                                 ##
            ####                                                  ##
             ###                                                  ##
             ##;                                                  ##
             ##$                                                 ##&
              ##                                                 ##
              ##;                                               ##
               ##                                              ##;
                ###                                          ###         ##$
                  ###                                      ###           ##
   ######################                              #####&&&&&&&&&&&&###
 ###        $#####$     ############&$o$&################################
 #                               $&########&o
'''

# Build-in / Std
import os, sys, time, platform, random
import re, json, cookielib

# requirements
import requests, termcolor, html2text
try:
    from bs4 import BeautifulSoup
except:
    import BeautifulSoup

# module
from auth import islogin
from auth import Logging


"""
    Note:
        1. 身份验证由 `auth.py` 完成。
        2. 身份信息保存在当前目录的 `cookies` 文件中。
        3. `requests` 对象可以直接使用，身份信息已经自动加载。

    By Luozijun (https://github.com/LuoZijun), 09/09 2015

"""
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard=True)
except:
    Logging.error(u"你还没有登录知乎哦 ...")
    Logging.info(u"执行 `python auth.py` 即可以完成登录。")
    raise Exception("无权限(403)")


if islogin() != True:
    Logging.error(u"你的身份信息已经失效，请重新生成身份信息( `python auth.py` )。")
    raise Exception("无权限(403)")


reload(sys)
sys.setdefaultencoding('utf8')

      


class Question:
    url = None
    soup = None

    def __init__(self, url, title=None):

        if not re.compile(r"(http|https)://www.zhihu.com/question/\d{8}").match(url):
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
        else:
            self.url = url

        if title != None: self.title = title

    def parser(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            'Host': "www.zhihu.com",
            'Origin': "http://www.zhihu.com",
            'Pragma': "no-cache",
            'Referer': "http://www.zhihu.com/"
        }
        r = requests.get(self.url,headers=headers, verify=False)
        self.soup = BeautifulSoup(r.content, "lxml")

    def get_title(self):
        if hasattr(self, "title"):
            if platform.system() == 'Windows':
                title = self.title.decode('utf-8').encode('gbk')
                return title
            else:
                return self.title
        else:
            if self.soup == None:
                self.parser()
            soup = self.soup
            title = soup.find("h2", class_="zm-item-title").string.encode("utf-8").replace("\n", "")
            self.title = title
            if platform.system() == 'Windows':
                title = title.decode('utf-8').encode('gbk')
                return title
            else:
                return title

    def get_detail(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        detail = soup.find("div", id="zh-question-detail").div.get_text().encode("utf-8")
        if platform.system() == 'Windows':
            detail = detail.decode('utf-8').encode('gbk')
            return detail
        else:
            return detail

    def get_answers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        answers_num = 0
        if soup.find("h3", id="zh-question-answer-num") != None:
            answers_num = int(soup.find("h3", id="zh-question-answer-num")["data-num"])
        return answers_num

    def get_followers_num(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        followers_num = int(soup.find("div", class_="zg-gray-normal").a.strong.string)
        return followers_num

    def get_topics(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        topic_list = soup.find_all("a", class_="zm-item-tag")
        topics = []
        for i in topic_list:
            topic = i.contents[0].encode("utf-8").replace("\n", "")
            if platform.system() == 'Windows':
                topic = topic.decode('utf-8').encode('gbk')
            topics.append(topic)
        return topics

    def get_all_answers(self):
        answers_num = self.get_answers_num()
        if answers_num == 0:
            print "No answer."
            return
            yield
        else:
            error_answer_count = 0
            my_answer_count = 0
            for i in xrange((answers_num - 1) / 20 + 1):
                if i == 0:
                    for j in xrange(min(answers_num, 20)):
                        if self.soup == None:
                            self.parser()
                        soup = BeautifulSoup(self.soup.encode("utf-8"), "lxml")

                        is_my_answer = False
                        if soup.find_all("div", class_="zm-item-answer")[j].find("span", class_="count") == None:
                            my_answer_count += 1
                            is_my_answer = True

                        if soup.find_all("div", class_="zm-item-answer")[j].find("div", class_="zm-editable-content clearfix") == None:
                            error_answer_count += 1
                            continue
                        author = None
                        if soup.find_all("div", class_="zm-item-answer-author-info")[j].get_text(strip='\n') == u"匿名用户":
                            author_url = None
                            author = User(author_url)
                        else:
                            author_tag = soup.find_all("div", class_="zm-item-answer-author-info")[j].find_all("a")[1]
                            author_id = author_tag.string.encode("utf-8")
                            author_url = "http://www.zhihu.com" + author_tag["href"]
                            author = User(author_url, author_id)

                        if is_my_answer == True:
                            count = soup.find_all("div", class_="zm-item-answer")[j].find("a", class_="zm-item-vote-count").string
                        else:
                            count = soup.find_all("span", class_="count")[j - my_answer_count].string
                        if count[-1] == "K":
                            upvote = int(count[0:(len(count) - 1)]) * 1000
                        elif count[-1] == "W":
                            upvote = int(count[0:(len(count) - 1)]) * 10000
                        else:
                            upvote = int(count)

                        answer_url = "http://www.zhihu.com" + soup.find_all("a", class_="answer-date-link")[j]["href"]

                        answer = soup.find_all("div", class_="zm-editable-content clearfix")[j - error_answer_count]
                        soup.body.extract()
                        soup.head.insert_after(soup.new_tag("body", **{'class': 'zhi'}))
                        soup.body.append(answer)
                        img_list = soup.find_all("img", class_="content_image lazy")
                        for img in img_list:
                            img["src"] = img["data-actualsrc"]
                        img_list = soup.find_all("img", class_="origin_image zh-lightbox-thumb lazy")
                        for img in img_list:
                            img["src"] = img["data-actualsrc"]
                        noscript_list = soup.find_all("noscript")
                        for noscript in noscript_list:
                            noscript.extract()
                        content = soup
                        answer = Answer(answer_url, self, author, upvote, content)
                        yield answer
                else:
                    post_url = "http://www.zhihu.com/node/QuestionAnswerListV2"
                    _xsrf = self.soup.find("input", attrs={'name': '_xsrf'})["value"]
                    offset = i * 20
                    params = json.dumps(
                        {"url_token": int(self.url[-8:-1] + self.url[-1]), "pagesize": 20, "offset": offset})
                    data = {
                        '_xsrf': _xsrf,
                        'method': "next",
                        'params': params
                    }
                    header = {
                        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                        'Host': "www.zhihu.com",
                        'Referer': self.url
                    }
                    r = requests.post(post_url, data=data, headers=header, verify=False)

                    answer_list = r.json()["msg"]
                    for j in xrange(min(answers_num - i * 20, 20)):
                        soup = BeautifulSoup(self.soup.encode("utf-8"), "lxml")

                        answer_soup = BeautifulSoup(answer_list[j], "lxml")

                        if answer_soup.find("div", class_="zm-editable-content clearfix") == None:
                            continue

                        author = None
                        if answer_soup.find("div", class_="zm-item-answer-author-info").get_text(strip='\n') == u"匿名用户":
                            author_url = None
                            author = User(author_url)
                        else:
                            author_tag = answer_soup.find("div", class_="zm-item-answer-author-info").find_all("a")[1]
                            author_id = author_tag.string.encode("utf-8")
                            author_url = "http://www.zhihu.com" + author_tag["href"]
                            author = User(author_url, author_id)

                        if answer_soup.find("span", class_="count") == None:
                            count = answer_soup.find("a", class_="zm-item-vote-count").string
                        else:
                            count = answer_soup.find("span", class_="count").string
                        if count[-1] == "K":
                            upvote = int(count[0:(len(count) - 1)]) * 1000
                        elif count[-1] == "W":
                            upvote = int(count[0:(len(count) - 1)]) * 10000
                        else:
                            upvote = int(count)

                        answer_url = "http://www.zhihu.com" + answer_soup.find("a", class_="answer-date-link")["href"]

                        answer = answer_soup.find("div", class_="zm-editable-content clearfix")
                        soup.body.extract()
                        soup.head.insert_after(soup.new_tag("body", **{'class': 'zhi'}))
                        soup.body.append(answer)
                        img_list = soup.find_all("img", class_="content_image lazy")
                        for img in img_list:
                            img["src"] = img["data-actualsrc"]
                        img_list = soup.find_all("img", class_="origin_image zh-lightbox-thumb lazy")
                        for img in img_list:
                            img["src"] = img["data-actualsrc"]
                        noscript_list = soup.find_all("noscript")
                        for noscript in noscript_list:
                            noscript.extract()
                        content = soup
                        answer = Answer(answer_url, self, author, upvote, content)
                        yield answer

    def get_top_i_answers(self, n):
        # if n > self.get_answers_num():
        # n = self.get_answers_num()
        j = 0
        answers = self.get_all_answers()
        for answer in answers:
            j = j + 1
            if j > n:
                break
            yield answer

    def get_top_answer(self):
        for answer in self.get_top_i_answers(1):
            return answer

    def get_visit_times(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        return int(soup.find("meta", itemprop="visitsCount")["content"])



