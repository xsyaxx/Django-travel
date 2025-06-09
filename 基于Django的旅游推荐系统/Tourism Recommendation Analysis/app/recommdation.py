import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
import django

# 基于目标用户和其他用户评分的相似度，推荐目标用户可能喜欢但没去过的旅游景点
# 它实现了一个经典的用户-用户协同过滤推荐系统，用的是余弦相似度来度量用户兴趣的相似度
os.environ.setdefault('DJANGO_SETTINGS_MODULE','去哪儿旅游数据分析推荐系统.settings')
django.setup()
from app.models import TravelInfo
# user_ratings = {
#     "Edward": {"南山文化旅游区": 5},
#     "EdwardD": {"南山文化旅游区": 5, "三亚蜈支洲岛旅游区": 2},
#     "newEdward"
# }
def getUser_ratings():
    user_ratings = {}
    for travel in TravelInfo.objects.all():
        comments = json.loads(travel.comments)
        for com in comments:
            try:
                com['userId']
            except:
                continue
            if user_ratings.get(com['userId'],-1) == -1:
                user_ratings[com['userId']] = {travel.title:com['score']}
            else:
                user_ratings[com['userId']][travel.title] = com['score']
    return user_ratings

def user_bases_collaborative_filtering(user_id,user_ratings,top_n=3):
    # 获取目标用户的评分数据
    target_user_ratings = user_ratings[user_id]

    # 初始化一个字段，用于保存其他用户与目标用户的相似度得分
    user_similarity_scores = {}

    # 将目标用户的评分转化为numpy数组
    target_user_ratings_list = np.array([
        rating for _ , rating in target_user_ratings.items()
    ])

    # 计算目标用户与其他用户之间的相似度得分
    for user,ratings in user_ratings.items():
        if user == user_id:
            continue
        # 将其他用户的评分转化为numpy数组
        user_ratings_list = np.array([ratings.get(item,0) for item in target_user_ratings])
        # 计算余弦相似度
        similarity_score = cosine_similarity([user_ratings_list],[target_user_ratings_list])[0][0]
        user_similarity_scores[user] = similarity_score

    # 对用户相似度得分进行降序排序
    sorted_similar_user = sorted(user_similarity_scores.items(),key=lambda x:x[1],reverse=True)

    # 选择 TOP N 个相似用户喜欢的景点 作为推荐结果
    recommended_items = set()
    for similar_user,_ in sorted_similar_user[:top_n]:
        recommended_items.update(user_ratings[similar_user].keys())

    # 过滤掉目标用户已经评分过的景点
    recommended_items = [item for item in recommended_items if item not in target_user_ratings]

    return recommended_items


if __name__ == '__main__':
    user_id =1
    user_ratings = getUser_ratings()
    recommended_items = user_bases_collaborative_filtering(user_id,user_ratings)
