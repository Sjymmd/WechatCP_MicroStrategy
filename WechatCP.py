# usr/bin/python3
# -*- coding : utf-8 -*-

from wechatpy.enterprise import WeChatClient
from wechatpy.enterprise.client.api import WeChatUser
from Conf import *
from Sql_Connect import SqlServer

import time

class Decorator(object):

    def __init__(self):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.corpsecret2 = corpsecret2
        self.agent_id = agentid
        self.party_id = department_id
        self.excel = excel
        self.excel_userlist = excel_userlist

    def print(*text):
        def decorator(func):
            def wrapper(*args,**kwargs):
                result = func(*args,**kwargs)
                lists = [*text,result]
                for list in lists:
                    if list is not None:
                        print(list,end='')
                print('')
            return wrapper
        return decorator

    def log(*text):

        import logging
        logging.basicConfig(filename='log.log',
                            format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S %p',
                            level=10)

        def decorator(func):
            def wrapper(self,*args,**kwargs):
                func(self,*args,**kwargs)
                words = []
                for word in text:
                    words.append( self.__getattribute__(word) ) if hasattr(self,word) else words.append(word)
                logging.log(10, 'log')
                logging.info(''.join(words))

            return wrapper
        return decorator

class WechatCp(Decorator):

    time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @Decorator.print(time)
    def __init__(self):
        super().__init__()

    @Decorator.print('推送完成')
    @Decorator.log('推送用户列表')
    def __call__(self, *args, **kwargs):

        if self.excel_userlist:
            self.__get_user_excel()
        else:
            self.__get_user()

        import getpass
        pwd = getpass.getpass('请输入数据库密码：')

        self.sqlServer = SqlServer(host, user, pwd, db)
        self.sqlServer()

        self.__send_messages(self.excel)

    @Decorator.print('根据企业微信列表获取用户信息列表：')
    def __get_user(self):

        client = WeChatClient(self.corpid, self.corpsecret)
        userlist = []
        weChatUser = WeChatUser(client)
        department_list = weChatUser.list(department_id,fetch_child=1)
        for users in department_list:
            userlist.append(users['userid'])

        self.userlist = userlist
        return self.userlist

    @Decorator.print('根据Excel表获取用户信息列表：')
    def __get_user_excel(self):

        import pandas as pd
        DataInf = pd.read_excel("push.xlsx")

        self.userlist = list(DataInf['user'])

        return self.userlist

    @Decorator.print('推送图文预警')
    def __send_messages(self,excel = False):

        client = WeChatClient(self.corpid, self.corpsecret2)

        if excel:
            import pandas as pd
            DataInf = pd.read_excel("push.xlsx")


        articles = [
            {
                "title": '子公司报表预警推送',
                "description":None,
                "url": 'http://58.211.172.130:7480/MicroStrategy/servlet/mstrWeb?evt=3140&src=mstrWeb.3140&documentID=E86C2E7041EB2C8079BF33A2C9B5D407&Server=ANS-MSTR&Project=Anyou_Mobile&Port=0&share=1&uid=dev&pwd=dev@anyou&hiddensections=header,path,dockTop,dockLeft,footer',
                "image": 'http://a3.att.hudong.com/64/06/01100000000000144728068606574_s.jpg'
            }]

        self.rate_media = client.media.upload(media_type='image', media_file=open('Rate.png', 'rb'))
        # self.ar_media = client.media.upload(media_type='image', media_file=open('AR.png', 'rb'))

        for users in self.userlist:

            if excel:
                articles = [
                    {
                        "title":DataInf.iloc[self.userlist.index(users),2] ,
                        "description": DataInf.iloc[self.userlist.index(users), 3],
                        "url": DataInf.iloc[self.userlist.index(users), 4],
                        "image": DataInf.iloc[self.userlist.index(users), 5]
                    }
                ]
            else:
                articles[0]['description'] = '%s请查收' % users

            client.message.send_articles(agentid, user_ids=users,articles=articles)
            # client.message.send_text(agentid, user_ids=users, content="%s 前，达成率小于50%%\n\n%s"%(self.sqlServer.today,self.sqlServer.Rate.to_string(index=False)))
            #
            # client.message.send_text(agentid, user_ids=users, content="%s 前，应收账款情况\n\n%s"%(self.sqlServer.today,self.sqlServer.AR.to_string(index=False)))
            client.message.send_image(agentid, user_ids=users, media_id=self.rate_media['media_id'], safe=0)

            # client.message.send_image(agentid, user_ids=users, media_id=self.ar_media['media_id'], safe=1)


if __name__ == '__main__':

    def main():
        wechatcp = WechatCp()
        wechatcp()

    # from apscheduler.schedulers.blocking import BlockingScheduler
    # sched = BlockingScheduler()
    # while True:
    #     # sched.add_job(main, 'interval', seconds=10)
    #     sched.add_job(main, 'cron', day='1,16', hour=8,misfire_grace_time=10)  # 定时每月1号和16号八点触发
    #     try:
    #         sched.start()
    #     except:
    #         print('定时任务出错')
    #         time.sleep(10)
    #         continue

    main()

