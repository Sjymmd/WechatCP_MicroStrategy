# -*- coding:utf-8 -*-
import pymssql
import datetime
# from Conf import host,user,db

class SqlServer:
    def __init__(self,host,user,pwd,db):

        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

        self.today = datetime.date.today()
        self.yesterday = self.today-datetime.timedelta(days=1)

    def __call__(self, *args, **kwargs):

        self.Rate = self.__Get_Rate()
        self.AR = self.__Get_AR()
        self.render_mpl_table(self.Rate, header_columns=0, col_width=2.0).get_figure().savefig('Rate.png')
        # self.render_mpl_table(self.AR,header_columns=0, col_width=2.0).get_figure().savefig('AR.png')


    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


    def __Get_Rate(self):

        reslist = self.ExecQuery("exec P_Warning_SalesYieldRate '%s'" % self.yesterday)
        list = []
        import pandas as pd

        for i in reslist:
            list.append(i)
            # print (i)
        df = pd.DataFrame(list, columns=['子公司', '销量 吨','达成率']).sort_values(by='达成率')
        if self.yesterday.day < 17:
            df = df[df["达成率"] < 0.5]

        df = df.reset_index(drop=True)

        for x in (df.index):
            df.iloc[x, -1] *= 100
            df.iloc[x, -1] = str('%d' % df.iloc[x, -1] + '%')
            df.iloc[x, -2] = round(df.iloc[x, -2],2)
        df = df.reset_index(drop=True)
        return df
        # return df.to_string(index=False)


    def __Get_AR(self):

        reslist = self.ExecQuery("exec P_Warning_AR '%s'" % self.yesterday)
        list = []
        import pandas as pd

        for i in reslist:
            list.append(i)
            # print (i)
        df = pd.DataFrame(list, columns=['子公司', '销量 万','销额 万','应收 万']).sort_values(by='应收 万',ascending=False)

        for x in range(1,4):
            df.iloc[:,x] = df.iloc[:,x].map(lambda x :int(x/10000))

        df = df.reset_index(drop=True)
        return df
        # return df.to_string(index=False)


    def render_mpl_table(self,data, col_width=3.0, row_height=0.625, font_size=14,
                         header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                         bbox=[0, 0, 1, 1], header_columns=0,
                         ax=None, **kwargs):
        import numpy as np
        import matplotlib.pyplot as plt
        import six

        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')

        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)
        fig.suptitle('子公司销量达成率报表', fontsize=32, y=0.94)
        fig.text(0.63,0.89 , self.yesterday.strftime("%Y年%m月%d日"),
                 fontsize=16, alpha=0.6)
        import random
        for x in range(1,4):
            fig.text(random.uniform(0.6,0.8),0.7-(x-1)*0.2, '安佑集团',
                     fontsize=50, color='gray',
                     ha='right', va='bottom', alpha=0.4)

        for k, cell in six.iteritems(mpl_table._cells):
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0] % len(row_colors)])
        return ax


if __name__ == '__main__':

    # sqlServer = SqlServer(host, user, pwd, db)
    # sqlServer()
    # print(sqlServer.AR )
    pass
    # newsql="update webuser set name='%s' where id=1"%u'测试'
    # ms.ExecNonQuery(newsql.encode('utf-8'))
