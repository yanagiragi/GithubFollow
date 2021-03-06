#-*- coding: utf-8 -*-
# Code by Ivan
# Automatically follow a lot of Github users which copy from a fixed user
# The first line of comments is English version
# The second line of comments is Chinese version
# They have the same meaning.Don't be confused
# Welcome to pull request
# Enjoy!
# Site:github.com/yfgeek

import os
import re
import sys
import urllib
import urllib2
import time
import cookielib

class GithubFollow(object):

    # Initializaiton Constructor
    # 初始化
    def __init__(self,name,password):
        self.user = name
        self.password = password
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)
        getCookieUrl = "https://github.com/login"
        self.html = urllib2.urlopen(getCookieUrl).read()

    # Browse the page to get Cookie
    # 模拟浏览器行为，得到Cookie
    def _get_headers(self,referer):
        headers = {}
        headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers['Connection']='keep-alive'
        headers['Cache-Control']='max-age=0'
        headers['Accept-Language']='zh-CN,zh;q=0.8,en;q=0.6'
        headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Referer']= referer
        return headers

    # sign up github
    # 方法登录网站
    def login(self):
        print "Getting the authenticity_token"
        token = self.__get_user_token(self.html)[0]
        loginparams = {
        'commit' : 'Sign in',
        'utf8' : '%E2%9C%93',
        'authenticity_token' : token,
        'login' : self.user,
        'password' : self.password
        }
        # post loginparams to login
        # post数据登录
        req = urllib2.Request( 'https://github.com/session', urllib.urlencode(loginparams), headers=self._get_headers('https://github.com/login'))
        tmp = 0
        try:
            resp = urllib2.urlopen(req)
        except :
            if (tmp <100):
                print 'Network conditions is not good.Reloading.'
                self.login(self)
            else:
                print 'Fail to get it' + img['src']
                pass
                tmp = tmp +1

        self.operate = self.opener.open(req)
        thePage = resp.read().decode("utf-8")
        # print the result of login
        # 查看登录结果
        print token
        print "Login Successful"
        return thePage

    # Get the userToken
    # 获取Token
    def __get_user_token(self,part):
        reg = re.compile('authenticity_token".*?value="(.*?)".*?>');
        result = re.findall(reg,part)
        return result
    def __get_user_list(self,part):
        reg = re.compile('link-gray.*?pl-1.*?>(.*?)</span>');
        result = re.findall(reg,part)
        return result
    def __follow_user(self,token,username):
        loginparams = {
        'utf8' : '%E2%9C%93',
        'authenticity_token' : token
        }
        # post loginparams to login
        # post数据登录
        req = urllib2.Request( 'https://github.com/users/follow?target='+username, urllib.urlencode(loginparams), headers=self._get_headers(''))
        try:
            resp = urllib2.urlopen(req)
        except Exception, e:
            print "Retrying..."
            self.__follow_user(self,token,username)
            pass
        else:
            pass
        self.operate = self.opener.open(req)
        thePage = resp.read().decode("utf-8")
        return thePage

    # get the userlist from a user who has a lot of followers
    # 获取复制用户的用户列表
    def list_follow(self,page,copyusername):
        url = "http://github.com/" + copyusername + "?page="+ str(page) +"&tab=following"
        req = urllib2.Request(url,headers=self._get_headers(''))
        try:
            response = urllib2.urlopen(req)
        except Exception, e:
            print "Retrying..."
        else:
            pass
        self.opener.open(req)
        thePage = response.read()
        tokenlist = self.__get_user_token(thePage)
        userlist = self.__get_user_list(thePage)
        for i in range(len(userlist)):
            time.sleep(1)
            print "\nIn the page "+ str(page) +", following the NO."+ str(i) +" user: " + userlist[i] + "\nToken：" + tokenlist[i]
            self.__follow_user(tokenlist[i],userlist[i])

if __name__ == '__main__':
    default_encoding = 'utf-8'
    if sys.getdefaultencoding() != default_encoding:
        reload(sys)
        sys.setdefaultencoding(default_encoding)
        # new object GithubFollow with parm1:username parm2:password
        #自动关注~ 用户名 密码
        gt = GithubFollow('username','password')
        # login
        # 登录
        gt.login()
        # range 1,100 is the page of follower page
        # range内是页数
        for i in range(100,10000):
            gt.list_follow(i,'chongbenben') #复制列表的人 The person who you want to copy his follower to yours
        print "Done."
