# _*_ encoding:utf-8 _*_
import sys, codecs
import re
from datetime import datetime

reload(sys)

sys.setdefaultencoding('utf8')


def getContentVecByStrs(strs, flag=False):
    # flag = False

    # a = datetime.now()
    dict_keys = []
    dict2 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFile\dict2.txt', 'r', 'utf-8')
    dict3 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFile\dict3.txt', 'r', 'utf-8')
    dict4 = codecs.open(r'F:\wushijia\workspace\medicineDialecticFile\dict4.txt', 'r', 'utf-8')
    words = codecs.open(r'F:\wushijia\workspace\medicineDialecticFile\words.txt', 'r', 'utf-8')
    dict2_lis = dict2.readlines()
    dict3_lis = dict3.readlines()
    dict4_lis = dict4.readlines()
    words_lis = words.read()
    dict2.close()
    dict3.close()
    dict4.close()
    words.close()

    words_lis = words_lis[1:len(words_lis)]

    res_num = []
    # str_lis = re.sub('\d+', '', str(''.join(lis)).replace(u' ', '')).strip('\n\r')
    # 将每个文件读出后去除空格
    str_num_dict2_lis = str(''.join(dict2_lis)).replace(u' ', u'')
    str_num_dict3_lis = str(''.join(dict3_lis)).replace(u' ', u'')
    str_num_dict4_lis = str(''.join(dict4_lis)).replace(u' ', u'')

    str_num_dictx_lis = ''

    # 将输入的字符串两两组合在文件dict2中进行比较
    for y in range(len(strs)):
        for z in range(len(strs)):
            if y < z:
                if not (strs[y].isdigit() or strs[z].isdigit()):
                    # 组合的内容如果非数字并且在dict文件中找到了，就放入dict_keys集合
                    if str_num_dict2_lis.find(strs[y] + strs[z]) is not -1:
                        inner = False
                        i = 1
                        while y + i < z:
                            # 如果某个组合第一个字与第二个字在整个字符串中中间有某个字在隔离字列表中，这个组合就不放入集合
                            if strs[y + i] in words_lis:
                                inner = True
                                break
                            i += 1
                        if not inner:
                            dict_keys.append(strs[y] + strs[z])

    # 将输入的字符串三个三个组合在文件dict3中进行比较，在dict3文件中匹配到的也放入dict_keys集合
    for w in range(len(strs)):
        for y in range(len(strs)):
            for z in range(len(strs)):
                if w < y < z:
                    if not (strs[w].isdigit() or strs[y].isdigit() or strs[z].isdigit()):
                        if str_num_dict3_lis.find(strs[w] + strs[y] + strs[z]) is not -1:
                            if flag:
                                inner = False
                                i = 1
                                while w + i < y:
                                    if strs[y+i] in words_lis:
                                        inner = True
                                        break
                                    i += 1
                                i = 1
                                while y + i < z:
                                    if strs[z+i] in words_lis:
                                        inner = True
                                        break
                                if not inner:
                                    dict_keys.append(strs[w] + strs[y] + strs[z])
                            else:
                                dict_keys.append(strs[w] + strs[y] + strs[z])

    # 四个四个组合
    for v in range(len(strs)):
        for w in range(len(strs)):
            for y in range(len(strs)):
                for z in range(len(strs)):
                    if v < w < y < z:
                        if not (strs[v].isdigit() or strs[w].isdigit() or strs[y].isdigit() or strs[z].isdigit()):
                            if str_num_dict4_lis.find(strs[v] + strs[w] + strs[y] + strs[z]) is not -1:
                                if flag:
                                    inner = False
                                    i = 1
                                    while v + i < w:
                                        if strs[v+i] in words_lis:
                                            inner = True
                                            break
                                        i += 1
                                    i = 1
                                    while w + i < y:
                                        if strs[w+i] in words_lis:
                                            inner = True
                                            break
                                        i += 1
                                    i = 1
                                    while y + i < z:
                                        if strs[y+i] in words_lis:
                                            inner = True
                                            break
                                        i += 1
                                    dict_keys.append(strs[v] + strs[w] + strs[y] + strs[z])
                                else:
                                    dict_keys.append(strs[v] + strs[w] + strs[y] + strs[z])

    # 将三个文件的内容组合成一个最终的字符串
    str_num_dictx_lis = str_num_dict2_lis + str_num_dict3_lis + str_num_dict4_lis

    # dict_keys集合中包含两个、三个、四个的组合，遍历集合中所有元素并在三个文件合成的字符串中进行查找
    # 查找每个元素在字符串前面的数字
    for x in dict_keys:
        # print x
        if re.findall(r'\d+', str(re.findall(r'\d+' + str(x), str(str_num_dictx_lis))))[0] not in res_num:
            res_num.append(re.findall(r'\d+', str(re.findall(r'\d+' + str(x), str(str_num_dictx_lis))))[0])

    # b = datetime.now()
    # print (b - a).seconds
    # for x in res_num:
    #     print x
    return res_num


strs = u'任某，女，33岁，首都机场门诊病历号131，初诊日期1966年3月25日。因腰背疼在积水潭医院、北京中医学院附院检查均诊断为“脊椎骨质增生”。近来头晕、头痛、目胀，下肢关节胀疼，手麻，乏力，四肢逆冷，易汗出，恶寒，苔白舌淡，脉沉细。'
# strs = u'头晕、腿痛'
print getContentVecByStrs(strs)
