import jieba
from matplotlib import pylab as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import json
import os
import django

# ✅ 1. 从数据库中读取旅游数据（TravelInfo 模型）
# ✅ 2. 对旅游介绍文本或评论内容做 分词（jieba）+ 停用词过滤
# ✅ 3. 生成漂亮的 中文词云图（WordCloud），并保存为图片文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE','去哪儿旅游数据分析推荐系统.settings')
django.setup()
from app.models import TravelInfo


def getIntroCloudImg(targetImgSrc,resImgSrc):
    travelList = TravelInfo.objects.all()
    text = ''
    stopwords = ['的', '是', '在', '这', '那', '他', '她', '它', '我', '你','和','等','为','有','与']
    for travel in travelList:
         text += travel.detailIntro

    cut = jieba.cut(text)
    newCut = []
    for tex in cut:
        if tex not in stopwords:
            newCut.append(tex)

    string = ' '.join(newCut)

    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )

    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off') # 不显示坐标轴

    # plt.show()

    plt.savefig(resImgSrc,dpi=500)


def getCommentContentCloudImg(targetImgSrc,resImgSrc):
    travelList = TravelInfo.objects.all()
    text = ''
    stopwords = ['的', '是', '在', '这', '那', '他', '她', '它', '我', '你','和','等','为','有','与']
    for travel in travelList:
        comments = json.loads(travel.comments)
        for comm in comments:
            text += comm['content']

    cut = jieba.cut(text)
    newCut = []
    for tex in cut:
        if tex not in stopwords:
            newCut.append(tex)

    string = ' '.join(newCut)

    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )

    wc.generate_from_text(string)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off') # 不显示坐标轴

    # plt.show()

    plt.savefig(resImgSrc,dpi=500)

if __name__ == '__main__':
    getCommentContentCloudImg('./static/2.jpg','./static/commentContentCloud.jpg')
