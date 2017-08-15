# _*_ encoding:utf-8 _*_
import MySQLdb

from utils.medicineVec import read4Vec


def getListout(lis):

    # maxMedicinexPRValtotall = 0.005
    medicinexPRValtotall = []
    res = []
    list_out = []

    # 返回到前端的标签
    return_labels = []
    second = False

    if lis.find(u"、") is not -1:
        num_lis = read4Vec(str(lis).split(u"、")[1])
        lis_structs = str(lis).split(u"、")[0]
        second = True
    else:
        num_lis = read4Vec(lis)
    conn = MySQLdb.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='w1020392881',
        db='candyonline',
        charset='utf8'
    )
    try:
        cursor = conn.cursor()
        medicinexPRVals = []
        symptomStrs = []
        dataSet = []
        listVecMax = []
        listVecMaxIndex = []
        for x in range(len(num_lis)):
            sql = "select medicine1PR,medicine2PR,medicine3PR,medicine4PR,medicine5PR,medicine6PR,medicine7PR," \
                  "medicine8PR,medicine9PR,medicine10PR,medicine11PR,medicine12PR,symptomPR,symptomStr from " \
                  "initial_cold_symptompr " \
                  "where symptomVec=" + num_lis[x]
            cursor.execute(sql)
            # 获取相应symptomVec所在行的medicine1PR...medicine12PR与symptomPR
            rs = cursor.fetchall()
            # 将每一个symptomVec中所在行的medicine1PR...medicine12PR与symptomPR相乘，并保留3位小数
            # print rs[-1][-1]
            for s in range(len(rs[0])-2):
                medicinexPRVals.append(round(float(rs[0][s]) * float(rs[0][-2]), 3))

        for x in range(12):
            # print sum(medicinexPRVals[x:len(medicinexPRVals)-1:12])
            if sum(medicinexPRVals[x:len(medicinexPRVals)-1:12]) not in medicinexPRValtotall:
                medicinexPRValtotall.append(sum(medicinexPRVals[x:len(medicinexPRVals)-1:12]))

        # 对不同元素的medicine1PRVal到medicine12PRVal的总和去除相同后进行从小到大排序
        for x in range(len(sorted(medicinexPRValtotall)[len(medicinexPRValtotall)-3:len(medicinexPRValtotall)])):
            res.append(sorted(medicinexPRValtotall)[len(medicinexPRValtotall) - 3:len(medicinexPRValtotall)][x])

        for r in reversed(res):
            list_out.append(medicinexPRValtotall.index(r)+1)

        # print list_out
        matrixA = filterMtrix(cursor, lis)
        # for x in matrixA:
        #     print x
        # 12PR列上每行元素分别与所在行symptomPR相乘
        for line in matrixA:
            for y in range(12):
                dataSet.append(round(float(line[y])*float(line[-2]), 3))

        # 获取12列中每一列的最大值在每一列中的位置
        for x in range(12):
            # if max(dataSet[x:len(dataSet):12]) not in listVecMax:
            listVecMax.append(max(dataSet[x:len(dataSet):12]))
            # listVecMaxIndex.append(dataSet[x:len(dataSet):12].index(max(dataSet[x:len(dataSet):12])))

        # for x in listVecMax:
        #     print x
            # if matrixA[x][-1] not in symptomStrs:
            #     symptomStrs.append(matrixA[x][-1])

        # for s in symptomStrs:
        #     print s

    finally:
        cursor.close()
        conn.close()


def filterMtrix(cursor, lis):
    """

    :param cursor:
    :param list_out:
    :return: 返回排除用户输入后的矩阵
    """
    # sql = "select "
    # for x in list_out:
    #     sql += "medicine" + str(x) + "PR,"
    # sql += "symptomVec,symptomPR from initial_cold_symptomPR where symptomStr not in ('" \
    #        + unicode(lis).replace(u'，', u'\',\'').split(u'。')[0] + "')"
    # cursor.execute(sql)
    sql = "select "
    for x in range(12):
        sql += "medicine" + str(x+1) + "PR,"
    sql += "symptomVec,symptomPR,symptomStr from initial_cold_symptompr where symptomStr not in ('" \
            + unicode(lis).replace(u'，', u'\',\'').split(u'。')[0] + "')"

    cursor.execute(sql)
    return cursor.fetchall()


lis = u'头痛，气喘，便干，咽痒，有痰，咳嗽，不欲饮，气短，呼吸困难，身痛。'
getListout(lis)
