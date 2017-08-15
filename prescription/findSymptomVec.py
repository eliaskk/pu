# _*_ encoding:utf-8 _*_
import MySQLdb

from utils.medicineVec import read4Vec


def getListout(lis):

    maxMedicinexPRValtotall = 0.01

    medicinexPRValtotall = []
    res = []
    list_out = []
    symptomRes = []
    lis_structs = ""
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
        index_res = []

        for x in num_lis:
            print x

        for x in range(len(num_lis)):
            sql = "select medicine1PR,medicine2PR,medicine3PR,medicine4PR,medicine5PR,medicine6PR,medicine7PR," \
                  "medicine8PR,medicine9PR,medicine10PR,medicine11PR,medicine12PR,symptomPR,symptomStr from " \
                  "initial_cold_symptompr " \
                  "where symptomVec=" + num_lis[x]
            cursor.execute(sql)
            # 获取相应symptomVec所在行的medicine1PR...medicine12PR与symptomPR
            rs = cursor.fetchall()
            # print rs[-1][-1]
            # 将每一个symptomVec中所在行的medicine1PR...medicine12PR与symptomPR相乘，并保留3位小数
            for s in range(len(rs[0])-2):
                medicinexPRVals.append(round(float(rs[0][s]) * float(rs[0][-2]), 3))

        # 将不同元素的medicine1PRVal到medicine12PRVal分别相加，有相同的则去除
        for x in range(12):
            # print sum(medicinexPRVals[x:len(medicinexPRVals)-1:12])
            if sum(medicinexPRVals[x:len(medicinexPRVals)-1:12]) not in medicinexPRValtotall:
                medicinexPRValtotall.append(sum(medicinexPRVals[x:len(medicinexPRVals)-1:12]))

        # print medicinexPRValtotall
        # 对不同元素的medicine1PRVal到medicine12PRVal的总和去除相同后进行从小到大排序
        for x in range(len(sorted(medicinexPRValtotall)[len(medicinexPRValtotall)-3:len(medicinexPRValtotall)])):
            res.append(sorted(medicinexPRValtotall)[len(medicinexPRValtotall) - 3:len(medicinexPRValtotall)][x])

        # print "排序后："
        # print res
        for r in reversed(res):
            list_out.append(medicinexPRValtotall.index(r)+1)

        # print "list_out:"
        # print list_out

        # print "medicinexPRValtotall len:"
        # print len(medicinexPRValtotall)
        # 得到排除用户输入后的矩阵
        # matrixA = cursor.fetchall()
        # filterMtrix(cursor, 12)
        matrixA = filterMtrix(cursor, 12, lis, second)
        # for x in matrixA:
        #     print x[-1]

        symptomStrs = []
        lis_res = []
        dataSet = []
        max_res = []

        # 将矩阵A中medicine1PR, ......, medicine12PR列上每个元素分别与symptomPR相乘
        for x in range(len(matrixA)):
            for y in list_out:
                dataSet.append(round(float(matrixA[x][y-1]) * float(matrixA[x][-2]), 3))
            symptomStrs.append(matrixA[x][-1])

        for x in range(len(list_out)):
            lis_res.append(max(dataSet[x:len(dataSet)-1:len(list_out)]))

        for x in range(len(lis_res)):
            index_res.append(dataSet[x:len(dataSet) - 1:len(list_out)].index(max(dataSet[x:len(dataSet) - 1:len(list_out)])))
            max_res.append(dataSet[x:len(dataSet)-1:len(list_out)].index(max(dataSet[x:len(dataSet)-1:len(list_out)])))

        if second:
            if max(res) > maxMedicinexPRValtotall:
                for x in index_res:
                    sql = "select medicineStr from initial_cold_medicinename where id=" + str(x)
                    cursor.execute(sql)
                    res = cursor.fetchall()
                    for x in res:
                        # print x[0]
                        if x[0] not in symptomRes:
                            symptomRes.append(x[0])
                symptomRes.insert(0, '1')
            else:
                for x in max_res:
                    if symptomStrs[x] not in symptomRes:
                        symptomRes.append(symptomStrs[x])
                symptomRes.insert(0, '0')
        else:
            for x in max_res:
                if symptomStrs[x] not in symptomRes:
                    symptomRes.append(symptomStrs[x])

    finally:
        cursor.close()
        conn.close()
    # print "symptomRes:........."
    # for x in symptomRes:
    #     print x
    return symptomRes


def filterMtrix(cursor, columns, lis, second):
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
    if second:
        for x in range(columns):
            sql += "medicine" + str(x+1) + "PR,"
        sql += "symptomVec,symptomPR,symptomStr from initial_cold_symptompr where symptomStr not in ('" \
                + unicode(lis).replace(u'，', u'\',\'').split(u'。')[0] + "')"
        sql = sql.replace(u'、', u'\',\'')
    else:
        for x in range(columns):
            sql += "medicine" + str(x+1) + "PR,"
        sql += "symptomVec,symptomPR,symptomStr from initial_cold_symptompr where symptomStr not in ('" \
                + unicode(lis).replace(u'，', u'\',\'').split(u'。')[0] + "')"
    # print sql
    cursor.execute(sql)
    return cursor.fetchall()


# lis = u'昨日受凉后，出现鼻流清涕，喷嚏，头痛，头晕，微恶风寒，咽痒，舌苔薄白浮黄，脉细数。'
# getListout(lis)
# print read4Vec(lis)
