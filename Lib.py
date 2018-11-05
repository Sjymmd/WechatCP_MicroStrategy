# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from Sql_Connect import *
import six
def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

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
    # # print(sqlServer.AR )
    #
    # # newsql="update webuser set name='%s' where id=1"%u'测试'
    # # ms.ExecNonQuery(newsql.encode('utf-8'))
    # df = sqlServer.Rate
    #
    # ax  = render_mpl_table(df, header_columns=0, col_width=2.0)
    # fig = ax.get_figure()
    # fig.savefig('Rate.png')


    # client.media.upload('image',)
    # client.message.send_image(agentid,user_ids=users,media_id='asdf.png')

    # from matplotlib.font_manager import _rebuild
    #
    # _rebuild()  # reload一下
    #
    # import pandas as pd
    # import numpy as np
    # list = [[1,2,3,4]]
    # data = pd.DataFrame(list, columns=[u'子公司', u'销量 万', u'销额 万', u'应收 万']).sort_values(by='应收 万', ascending=False)
    # size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([3, 0.625])
    # fig, ax = plt.subplots(figsize=size)
    # # plt.rcParams['font.sans-serif'] = ['SimHei']
    # mpl_table = ax.table(cellText=data.values, bbox=[0, 0, 1, 1], colLabels=data.columns,)
    # figure = mpl_table.get_figure()
    # fig.suptitle('',fontsize=16,x=0.53,y=1.05,)
    # figure.show()

    from matplotlib.font_manager import FontManager
    import subprocess

    # fm = FontManager()
    # mat_fonts = set(f.name for f in fm.ttflist)
    # # print(mat_fonts)
    # output = subprocess.check_output('fc-list :lang=zh -f "%{family}\n"', shell=True)
    # # print( '*' * 10, '系统可用的中文字体', '*' * 10)
    # # print (output)
    # zh_fonts = set(f.split(',', 1)[0] for f in output.decode('utf-8').split('\n'))
    # available = mat_fonts & zh_fonts
    # print('*' * 10, '可用的字体', '*' * 10)
    # for f in available:
    #     print(f)

    # from PIL import Image, ImageDraw
    #
    # def add_watermark_to_image(image, watermark):
    #     rgba_image = image.convert('RGBA')
    #     rgba_watermark = watermark.convert('RGBA')
    #
    #     image_x, image_y = rgba_image.size
    #     watermark_x, watermark_y = rgba_watermark.size
    #
    #     # 缩放图片
    #     scale = 10
    #     watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
    #     new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
    #     rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)
    #     # 透明度
    #     rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 180))
    #     rgba_watermark.putalpha(rgba_watermark_mask)
    #
    #     watermark_x, watermark_y = rgba_watermark.size
    #     # 水印位置
    #     rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), rgba_watermark_mask)
    #
    #     return rgba_image
    #
    # im_before = Image.open("Rate.png")
    # im_before.show()
    #
    # im_watermark = Image.open("AR.png")
    # im_after = add_watermark_to_image(im_before, im_watermark)
    # im_after.show()
    # im.save('im_after.jpg')

    import random

    for x in range(1, 4):
       print(random.uniform(0.3,0.8))