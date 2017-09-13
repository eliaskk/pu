# _*_ encoding:utf-8 _*_
import re
import time
import MySQLdb
import sys

from utils.medicineVec import strlineWord2par2, strlineWord2par3, strlineWord2par4

reload(sys)

sys.setdefaultencoding('utf8')


def batchWrite(conn, table, fileName):
    """ 读取文件批量写入数据库

    :param conn: 数据库连接
    :param table: 要操作的数据表
    :param fileName: 文件的绝对路径
    :return:
    """

    sourceFrom = fileName[fileName.find(".txt") + 4:]
    fileName = fileName[:fileName.find(".txt") + 4]

    if sourceFrom == '':
        sourceFrom = u''
    else:
        sourceFrom = unicode(sourceFrom)

    # print isinstance(sourceFrom, unicode)
    f = open(fileName, 'r')
    cursor = conn.cursor()
    try:
        # 病名
        diseaseNames = []
        # 开方名
        prescriptionNames = []
        # 患者
        patientContents = []
        # 开方
        prescriptions = []
        # 开方原因
        prescriptionsReasons = []

        for line in f:
            content = unicode(line, 'utf-8')
            if content.startswith(u'病名：'):
                diseaseName = content[3:]
                diseaseNames.append(diseaseName)
            elif content.startswith(u'开方：'):
                str = content[3:]
                # 开方名
                prescriptionName = str[0:str.find(u"：")]
                # 开方
                prescription = str[str.find(u"：") + 1:]
                prescriptionNames.append(prescriptionName)
                prescriptions.append(prescription)
            elif content.startswith(u'主诉：'):
                str = content[3:]
                patientContents.append(str)
            elif content.startswith(u'开方原因：'):
                prescriptionsReasons.append(content[5:])

        lis = []
        print "diseaseNames", len(diseaseNames)
        print "patientContent", len(patientContents)
        print "prescriptionNames", len(prescriptionNames)
        print "prescriptions", len(prescriptions)
        print "prescriptionsReasons", len(prescriptionsReasons)
        for x in range(len(diseaseNames)):
            print diseaseNames[x]
            print patientContents[x]
            print prescriptionNames[x]
            print prescriptions[x]
            print prescriptionsReasons[x]

            # print sourceFrom

            sql = "insert into "+table+"(diseaseName,patientContent,prescriptionName,prescriptions,prescriptionsReason,sourceFrom) VALUES (" \
                                       "%s,%s,%s,%s,%s,%s)"

            select = "select id from " + table + " where patientContent='" + patientContents[x] + "'"
            if cursor.execute(select) > 0:
                print u"数据已存在"
                cursor.close()
                conn.commit()

            data = (diseaseNames[x], patientContents[x], prescriptionNames[x], prescriptions[x], prescriptionsReasons[x], sourceFrom)
            lis.append(data)
            print cursor.executemany(sql, lis)
            del lis[:]
    except MySQLdb.Error as e:
        print e
        conn.rollback()
    finally:
        conn.commit()
        cursor.close()
        f.close()


def insertmany(conn, table, field, value):
    """ 插入多个字段值

    :param conn: 数据库连接
    :param table: 操作的数据表
    :param field: 插入的字段，之间用英文状态下逗号隔开
    :param value: 插入的字段值，之间用英文状态下逗号隔开
    :return: 返回影响的行数
    """
    value = value.split(',')
    str = '\',\''
    cursor = conn.cursor()
    try:
        sql = "insert into " + table + "(" + field + ") VALUES ('" + str.join(value) + "')"
        res = cursor.execute(sql)
    finally:
        conn.commit()
        cursor.close()
    return res


def select(conn, table, field, value, field2):
    """ 根据指定条件字段查询字段

    :param conn: 数据库连接
    :param table: 操作的数据表
    :param field: 作为查询条件的字段
    :param value: 作为查询条件的字段值
    :param field2: 要查询的字段
    :return: 返回查询字段的值的结果集
    """
    res = ""

    field = transcoding(field)
    value = transcoding(value)
    field2 = transcoding(field2)
    cursor = conn.cursor()
    try:
        sql = "select " + field2 + " from " + table + " where " + field + "='" + value + "'"
        cursor.execute(sql)
        res = cursor.fetchall()
    finally:
        conn.commit()
        cursor.close()

    return res


def deleteById(conn, table, id):
    """ 根据id删除行

    :param conn: 数据库连接
    :param table: 要操作的数据表
    :param id: 根据id删除行数据
    :return: 返回影响的行数
    """
    res = 0
    cursor = conn.cursor()
    try:
        sql = "delete from " + table + " where id = " + id
        res = cursor.execute(sql)
    finally:
        conn.commit()
        cursor.close()
    return res


def recoginzePrescriptions(conn, input):
    """  根据药方组合辨识药名

    :param conn: 数据库连接
    :param input: 输入的药方，药方之间用英文逗号隔开
    :return: 返回查询的结果集
    """
    prescriptionNames = []
    f = ''

    sql = "select singleMedicine from single"
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rs = cursor.fetchall()
        cursor.execute("select * from prescription")
        f = cursor.fetchall()
    finally:
        cursor.close()
    singles = input.split(u'，')

    for k in range(len(singles)):
        for j in rs:
            if singles[k].find(j[0]) is not -1:
                singles[k] = j[0]

    index = []
    res = []

    for line in f:
        # print line[1] 药名
        # print line[2] 药方
        prescription2 = re.split(u'，|/|\\n', line[2])
        tmp = list(set(prescription2).intersection(set(singles)))
        index.append(len(tmp))

    for x in range(len(index)):
        # 如果集合中某个数是该集合最大的数，记下该数在数列中的位置
        if index[x] == max(index):
            res.append(x)

    for x in res:
        prescriptionNames.append(f[x][1])
    return prescriptionNames


def getByContentVec(conn, table, fileName, lis):
    """ 读取包含输入的contentVec所在行，并输出到文件

    :param conn: 数据库连接
    :param table: 要操作的数据表
    :param fileName: 存放输出文件的文件夹路径
    :param lis: 输入的contentVec
    :return:
    """
    cursor = conn.cursor()
    f = open(fileName, 'w')
    try:
        sql = "select * from "+table
        cursor.execute(sql)
        rs = cursor.fetchall()
        for x in rs:
            if x[3] is not None:
                union = list(set(unicode(x[3]).split(u'，')).intersection(set(lis)))
                if len(union) == len(lis):
                    # f.write('ID'+str(x[0])+' '+x[3]+'\n')
                    for y in x:
                        if str(y).find('\n') is not -1:
                            f.write(str(y)[:str(y).find('\n')]+'\n')
                        else:
                            f.write(str(y)+'\n')
    finally:
        cursor.close()
        f.close()


def contrastContentVec(conn, table, fileName):
    """ 对比表中contentVec字段的值，将两两相等值所在的行导出到文本文件

    :param conn: 数据库连接
    :param table: 要操作的数据表
    :param fileName: 存放输出文件的文件夹路径
    :return:
    """
    cursor = conn.cursor()
    try:
        sql = 'select * from '+table+' as A where' \
                                     '(contentVec IN(select contentVec from '+table+' as B where A.ID<>B.ID))'
        cursor.execute(sql)
        rs = cursor.fetchall()
        f = open(fileName, 'w')
        for x in rs:
            for y in x:
                if str(y).find('\n') is not -1:
                    f.write(str(y)[:str(y).find('\n')] + '\n')
                else:
                    f.write(str(y) + '\n')
    finally:
        cursor.close()
        f.close()


def updateContentVecByFile(conn, table, fileName):
    """ 读取文件根据id批量修改contentVec字段中的值
        （待优化）
    :param conn: 数据库连接
    :param table: 要操作的数据表
    :param fileName: 读取的文件的绝对路径
    :return:
    """
    f = open(fileName, 'r')
    cursor = conn.cursor()
    try:
        for line in f:
            if line.find(',') is not -1:
                line = line.replace(',', u'，')
            contentVec = line[line.find(u' ')+1:]
            id = line[2:line.find(u' ')]
            sql = "update "+table+" set contentVec='"+contentVec+"' where id="+id
            print cursor.execute(sql)
    finally:
        conn.commit()
        cursor.close()


def updateContentVecByFileNoId(conn, table, fileName):
    f = open(fileName, 'r')
    cursor = conn.cursor()
    try:
        x = 0
        ids = "("
        sql = "update "+table+" set contentVec = case id "
        for line in f:
            x+=1
            ids += str(x)+","
            sql += "when "+str(x)+" then '"+line+"'"
            # print x,line
        sql += "end where id in "+ids[:-1]+")"
        print cursor.execute(sql)
    finally:
        conn.commit()
        cursor.close()


def getContentVecByWord(conn, table, keyword, filePath):
    """ 根据patientContent关键词返回行号ID，contentVec值到新生成的文本文件中

    :param conn: 数据库连接
    :param table: 操作的数据表
    :param keyword: 关键词
    :param filePath: 存放输出文本文件的文件夹路径
    :return:
    """
    keyword = keyword.replace(u' ', '')
    fileName = keyword+'_patientContent_'
    fileName += time.strftime('%Y-%m-%d', time.localtime(time.time()))+'.txt'
    sql = "select * from "+table
    cursor = conn.cursor()
    fp = open(filePath + '\\' + fileName, 'a+')
    try:
        cursor.execute(sql)
        rs = cursor.fetchall()
        for x in rs:
            if len(keyword) is 2:
                if strlineWord2par2(x[2], keyword[0], keyword[1]):
                    print x[0]
                    print x[3]
                    fp.writelines("ID"+str(x[0])+" "+str(x[3])+"\n")
            elif len(keyword) is 3:
                if strlineWord2par3(x[2], keyword[0], keyword[1], keyword[2]):
                    print x[0]
                    print x[3]
                    fp.writelines("ID"+str(x[0])+" "+str(x[3])+"\n")
            elif len(keyword) is 4:
                if strlineWord2par4(x[2], keyword[0], keyword[1], keyword[2], keyword[3]):
                    print x[0]
                    print x[3]
                    fp.writelines("ID"+str(x[0])+" "+str(x[3])+"\n")
    finally:
        cursor.close()
        fp.close()


def getNumByPrescriptionN(cinput):
    """ 调用getNumByPrescriptionName方法根据药方名或药方组成获取主药方相应的编号

    :param cinput:药方名或药方组成或文件绝对路径，文件必须以.txt结尾
    :return: 返回获取到的主药方相应的编号，若输入参数为文件，完成后返回finish
    """

    drug_dict = open(r'F:\wushijia\workspace\613\drug_dict.txt', 'r')
    medicineName = open(r'F:\wushijia\workspace\613\medicineName.txt', 'r')
    try:
        medicineNameReadLines = medicineName.readlines()
        drugDictRead = drug_dict.read()
    finally:
        drug_dict.close()
        medicineName.close()
    # print getNumByPrescriptionName(cinput, drug_dict, medicineName.readlines())

    if not isinstance(cinput, unicode):
        cinput = unicode(cinput)

    if cinput.find(u'克') is not -1:
        cinput = cinput.replace(u'克', '')
    elif cinput.find(u'g') is not -1:
        cinput = cinput.replace(u'g', '')
    regex = re.compile(ur',|、| |。|，')
    cinput = regex.sub(',', cinput)
    cinput = re.sub('\d+', '', cinput)

    if cinput.find(u',') is not -1:
        tmplis = getNumByPrescriptionName(cinput, drugDictRead, medicineNameReadLines)
        return tmplis
    elif cinput.find('.txt') is not -1:
        fileName = open(cinput, 'r')
        outFileName = open(cinput[:cinput.find('.txt')] + '_output' + cinput[cinput.find('.txt'):], 'w')
        for line in fileName:
            line = line.replace(u'克 ', ',').replace(u'克', '')
            line = re.sub('\d+', '', line)
            # print line
            outFileName.writelines(getNumByPrescriptionName(line, drugDictRead, medicineNameReadLines)+'\n')
        outFileName.close()
        fileName.close()
        return 'finish'
    else:
        for line in medicineNameReadLines:
            line = unicode(line)
            if line[line.find(u' ')+1:line.find(u'：')] in cinput:
                res = line[:line.find(u' ')]

        return res


#
def getNumByPrescriptionName(cinput, drug_dict, medicineName):
    """ 根据药方名或药方组成获取主药方相应的编号，供getNumByPrescriptionN方法调用

    :param cinput: 药方组成
    :param drug_dict: drug_dict文件
    :param medicineName: medicineName文件
    :return: 返回相应的编号
    """
    drug_dicts = unicode(drug_dict)
    mode = re.compile(r'\d+')
    medicineNames = []
    medicineNames_dict_lines = []
    medicineNames_dict_lens_count = 0
    union_lis = []
    union_len = 0
    res_index = ''
    w=0
    for medicineNameLine in medicineName:
        num_lis = []
        medicineNameLine = unicode(medicineNameLine)
        if medicineNameLine.find(u'\n') is not -1:
            medicineNames.append(medicineNameLine[:medicineNameLine.find(u'\n')])
            # 匹配参数中的分隔符
            line_lis = medicineNameLine[medicineNameLine.find(u'：') + 1:medicineNameLine.find(u'\n')].split(u',')
        else:
            medicineNames.append(medicineNameLine[:])
            line_lis = medicineNameLine[medicineNameLine.find(u'：'):].split(u',')

        # 每一行分割后的列表在drug_dict中对应的数字
        for x in line_lis:
            ma = re.findall(u'\d*_*\d' + x + '\n', drug_dicts.replace(u' ', ''))
            # 将每一行分割后的元素放入集合
            if x not in medicineNames_dict_lines:
                medicineNames_dict_lines.append(x)
            # 将每一行分割后的元素对应drug_dict中的数字放入集合
            for y in ma:
                num_lis.append(mode.findall(y)[0])

        # 获取每一行加上drug_dict中的同义词
        for line in drug_dicts.split(u'\n'):
            for x in num_lis:
                # 将每一行分割后的元素所有同义词加入集合
                if line.startswith(u'' + x + u' ') or line.startswith(u'' + x + u'_'):
                    if line[line.find(u' ') + 1:] not in medicineNames_dict_lines:
                        medicineNames_dict_lines.append(line[line.find(u' ') + 1:])

        # 记录每一行元素的数量

        union_lis = list(set(medicineNames_dict_lines).intersection(cinput.split(u',')))

        # print '--------------------------'

        if len(union_lis) > union_len:
            union_len = len(union_lis)
            res_index = medicineNameLine[:medicineNameLine.find(u' ')]
            medicineNames_dict_lens_count = len(medicineNames_dict_lines)
        elif len(union_lis) == union_len:
            if len(medicineNames_dict_lines) < medicineNames_dict_lens_count:
                medicineNames_dict_lens_count = len(medicineNames_dict_lines)
                res_index = medicineNameLine[:medicineNameLine.find(u' ')]

        del medicineNames_dict_lines[:]
    return res_index


def transcoding(field):
    """ 编码转换，将输入的参数转为unicode

    :param field: 输入的内容
    :return: 转换为unicode后返回
    """
    if not isinstance(field, unicode):
        return unicode(field, "gbk", "ignore")
    else:
        return field


def command_toast(text):
    """ 将命令行输入的参数转换为unicode

    :param text: 要转换的内容
    :return: 转换后的内容
    """
    return text.encode('gbk', 'ignore')
    # return unicode(text)


def command():
    """ 调用该函数在命令行中进行操作

    :return:
    """
    host = transcoding(raw_input(command_toast("请先初始化数据库\n请输入主机名：")))
    user = transcoding(raw_input(command_toast("请输入用户名：")))
    pwd = transcoding(raw_input(command_toast("请输入密码：")))
    db = transcoding(raw_input(command_toast("请输入数据库名：")))
    conn = MySQLdb.connect(host, user, pwd, db, use_unicode=True, charset="utf8")
    loop(conn)
    conn.close()
    print "\nexit"


def loop(conn):
    """ 在命令行中完成一个操作后不退出程序，调用该函数继续进行数字选择，直至手动选择退出

    :param conn: 数据库连接
    :return:
    """
    try:
        toast = command_toast("请输入要执行的函数：1.读取文件批量写入数据库 2.添加数据 3.查询字段 4.删除数据"
                              " 5.根据药方组合辨识药名 6.输入list，统计同时出现在contentVec中的数字 7.对比数据表中contentVec两两相等的值 "
                              "8.批量更新contentVec中的值 9.根据关键词获取contentVec 10.根据药方名或药方组成获取主药方相应的编号"
                              " 0.退出\n")
        res = transcoding(raw_input(toast))
        if res == u'1':
            try:
                table = raw_input(command_toast("请输入表名："))
                res1 = raw_input(command_toast("请输入要读取的文件绝对路径+来源，默认来源为：胡希恕伤寒方证辩证 "))
                res1 = unicode(res1, "gbk", "ignore")
                if res1.find(".txt") is not -1:
                    batchWrite(conn, table, res1)
                    loop(conn)
                else:
                    print command_toast("输入的参数不正确")
            except Exception as e:
                print command_toast("输入的参数不正确")
        elif res == u'0':
            return
        elif res == u'2':
            table = transcoding(raw_input(command_toast("请输入表名：")))
            field = transcoding(raw_input(command_toast("请输入要插入的字段名，并用逗号隔开：")))
            value = raw_input(command_toast("请输入要插入的字段值，并用逗号隔开："))
            insertmany(conn, table, field, value)
            loop(conn)
        elif res == u'3':
            table = transcoding(raw_input(command_toast("请输入表名：")))
            field = transcoding(raw_input(command_toast("请输入条件字段：")))
            value = transcoding(raw_input(command_toast("请输入条件字段值：")))
            field2 = transcoding(raw_input(command_toast("请输入要查询的字段：")))
            for x in select(conn, table, field, value, field2):
                print x[0]
            loop(conn)
        elif res == u'4':
            table = transcoding(raw_input(command_toast("请输入表名：")))
            id = transcoding(raw_input(command_toast("请输入要删除的id：")))
            print deleteById(conn, table, id)
            loop(conn)
        elif res == u'5':
            prescriptions = transcoding(raw_input(command_toast("请输入药方组合，药方之间用英文逗号隔开：")))
            for x in recoginzePrescriptions(conn, prescriptions):
                print x
            loop(conn)
        elif res == u'6':
            table = transcoding(raw_input(command_toast("请输入要操作的数据表：")))
            fileName = transcoding(raw_input(command_toast("请输入要输出的文件路径：")))
            lis = transcoding(raw_input(command_toast("请输入要统计的list，元素之间用中文逗号隔开：")))
            # ['89', '182', '9', '52']
            getByContentVec(conn, table, fileName, lis.split(u','))
            loop(conn)
        elif res == u'7':
            table = transcoding(raw_input(command_toast("请输入要操作的数据表：")))
            fileName = transcoding(raw_input(command_toast("请输入要输出的文件路径：")))
            contrastContentVec(conn, table, fileName)
            loop(conn)
        elif res == u'8':
            table = transcoding(raw_input(command_toast("请输入要操作的数据表：")))
            fileName = transcoding(raw_input(command_toast("请输入要读取的文件路径：")))
            updateContentVecByFile(conn, table, fileName)
            loop(conn)
        elif res == u'9':
            table = transcoding(raw_input(command_toast("请输入要操作的数据表：")))
            keyword = transcoding(raw_input(command_toast("请输入关键字：")))
            filePath = transcoding(raw_input(command_toast("请输入输出文件的存放路径：")))
            getContentVecByWord(conn, table, keyword, filePath)
            loop(conn)
        elif res == u'10':
            cinput = transcoding(raw_input(command_toast("请输入药方名或药方组成（可输入批量文件）：")))
            print getNumByPrescriptionN(cinput)
            loop(conn)
        else:
            print command_toast("输入的参数不正确")
    except Exception as e:
        print command_toast("输入的参数不正确")
        conn.rollback()
    finally:
        return


def callBatchWrite():
    conn = MySQLdb.connect("127.0.0.1", "root", "w1020392881", "candyonline", use_unicode=True, charset="utf8")
    # conn = MySQLdb.connect("39.108.2.147", "root", "Jaris->pwd=w1020392881", "candyonline", use_unicode=True, charset="utf8")
    batchWrite(conn, "medicine_operation", r'F:\wushijia\workspace\912\pmtotall0912.txt')
    conn.close()

# command()
# callBatchWrite()
