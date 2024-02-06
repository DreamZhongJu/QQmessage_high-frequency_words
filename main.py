'''
该程序是用来统计QQ聊天记录高频词的
将QQ聊天记录从电脑端导出为.txt格式，并按照一下注释修改相关变量即可实现统计高频词、
如果不想改动太多变量，只用修改文件路径和文件名即可（在下面）
'''


from collections import Counter, OrderedDict
import jieba
import pandas as pd
import zhconv
import re




#######################添加特殊词###########################
add_list= [
    #在这里键入你想要添加的特殊词
    "古明地恋",
    "希腊奶",
    "zun"
]
jieba.add_word("".join(str(i) for i in add_list))
###########################################################




def hans_2_hant(hans_str: str):#转换简体
    return zhconv.convert(hans_str, 'zh-cn')




#######################过滤QQ所有消息头######################
def checking(strLine:str)->bool:
    res = re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}',strLine)
    if res:
        return False
    else:
        return True
###########################################################




#删除标点符号
stopwords=[
    '：',
    '“',
    '！',
    '”',
    '\n',
    '《',
    '》',
    '【',
    '】',
    ' ',
    '——',
    '，',
    '—',
    '、'
]

################文件所在路径以及文件名#################
path = "（在这里输入聊天记录所在路径）"
name = r'（在这里输入聊天记录文件名）.txt'
###################################################



file = open(path+name,'r', encoding='utf-8')
#生成处理文本
processFile = open(path+'处理.txt','w', encoding='utf-8')
#开始处理文本
word_list=[]
for i in file.readlines():
    if checking(i):
        newStr = re.sub(r'@\S+\s|\[\w{2}\]|请使用最新版手机QQ体验新功能|音视频通话已结束|.*撤回了一条消息\w*|\n|邀请|加入本群|Auditore|[暂不支持该消息类型，请用手机QQ查看]|/答\w|\w*共同好友点击添加好友|@　　　　　　　　|^/\w*|\[\]|抽奖 \d+.{1}\d*|输入有效积分|/知识问答 ','',i)
        if newStr:
            processFile.write(newStr+'\n')
        word_list += jieba.cut(newStr)
#输出处理文本
processFile.close()
#处理文本，并过滤长度不超过1的文本
word_list = pd.Series(word_list)[pd.Series(word_list).apply(len) > 1]
word_list = word_list[~word_list.isin(stopwords)]
word_list = Counter(word_list)

#开始计数
charCounter = OrderedDict(word_list.most_common())

counter = 0

#创建高频词文本
newFile = open(path+'高频词汇.txt','w', encoding='utf-8')


for i in charCounter:
    print(i,':',charCounter[i])
    newFile.write(i+':'+str(charCounter[i]))
    newFile.write('\n')
    counter += 1
    if counter == 99:
        break