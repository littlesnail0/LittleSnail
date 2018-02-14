import requests
import itchat
import time
import random
import os
from aip import AipSpeech
from pydub import AudioSegment

""" 你的 APPID AK SK """
APP_ID = '10544044'
API_KEY = 'BQBg3oGPnrFrAulmsDazTPpL'
SECRET_KEY = '87b82d43edaed4be69fc4bed803f0feb'


client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
KEY = '8edce3ce905a4c1dbb965e6b35c3834d' # Turing Machine Online Access Token
snailRobot = itchat.new_instance()
commandRobot = itchat.new_instance()

number_version = ["2017-11-25 16:21我们第一次联系\r\n2017-12-05 00:02 我第一次说想你\r\n2017-12-09 00:46 冲动地说了对你的喜欢", "到情人节恰好81天，久久归真(～～)", "数字一下微信记录",  "喜欢出现668条", "厉害出现268条", "想你出现198次", "晚安出现189条", "梦出现了162条", "呼唤了小蜗牛67次", "..... 还有好多好多关键词", "哦对了， 嗯这次出现了4141次(好多)......", "我一直很喜欢数字，因为很多数字有魔力","虽然这一次我强行统计的这些数字并不见得有什么magic","但是它们如此真实而有趣而且就在那不经意的长大。","甚至不觉间感受了这些数字的分量，就好像我对你的喜欢一点点一天天在累积....", "我相信数字有魔力，也许等到量变到质变的那一天，它们就会展现...","希望在以后每一个情人节的时候，看着这些数字不断变大，就像我们的情谊会不断滋长.......", "Let there be love ～， that is more magical than numbers"]
romantic_version = ["一直都在对你说遇见你是我的幸运", "当要对你说得什么时，就会莫名想起你带给我的那些第一次", "第一次头疼你陪我给我讲拥抱的感受\r\n第一次给我起外号\r\n第一次知道白开水的叹息\r\n第一次看你画\r\n第一次听你那么多经历", "你是如此有趣，和你交流听你诉说让我第一次感受到温暖", "第一次你给我讲故事\r\n第一次你给我听你唱的歌曲\r\n第一次电话\r\n", "第一次你说想我\r\n第一次你说喜欢我\r\n", "你是如此可爱热情，我第一次发现声音也这么迷人，心也变得柔软",
"第一次的礼物\r\n第一次收到的水果\r\n还有听见你哭\r\n听到你说情动","直到再次遇见时，牵手、拥抱、第一个吻.......还有那像梦一样的时刻不分的一周", "我的世界就这样因你而改变，如此简单而奇妙",
"还要对你说什么时,我却想从不好的说起，没办法两面性是我的风格,一面随性一面封闭， 。", 
"我们都不完美，特别是我有很多很多的不好，不够成熟，温温吞吞，不够体贴，懒散、邋遢甚至有些纠结、敏感.......还有很多","并且我也知道那些都很难再改变", "然后我还明白我们之间就算再奇妙也还是面临很多困难，那些都可能会让我纠结、犹疑、变得不自信甚至会传染给你.....", "但是，我曾经说过我从不后悔自己的决定，当我说过认定你的那一刻就算是带着冲动也罢，就算之后遇到一些事我也会起波澜也会心烦浮躁也会自卑气馁(这些我都会慢慢去改变)也罢，只要一想到你一想到我不会后悔那些也会让我变得愈发坚定", "因为我知道越美好的事物越要付出努力，因为我喜欢的样子你都有，因为我愿意为你而变得更好", "只因为我想和你在一起"]
code_version = "code_version"

POEMS = {}

def series_send_msg(author, series):
    for sentence in series:
        author.send(sentence)
        time.sleep(4)

    return


def send_image(author):
    author.send("代码就不看啦，我把你的照片拼成了下面这一张")
    time.sleep(3)
    snailRobot.send_image('pictures/love.jpg', author.UserName)
    author.send("然后在上面加了颗心，yeah～")
    time.sleep(3)
    i = random.randint(1, 7)
    fname = 'pictures/{}.png'.format(i)
    snailRobot.send_image(fname, author.UserName)



def get_turing_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


# 回复消息封装
def text_reply(message):
    robots_reply = get_turing_response(message)
    if robots_reply:
        return robots_reply
    else:
        return '一时不知道怎么接' + '(其实是后台出错解析)'


# 语音消息处理
def voice_reply(msg):
    msg.download(msg.fileName)
    # 转换为wav格式的文件
    sound = AudioSegment.from_mp3(msg.fileName)
    sound.export(msg.fileName, format="wav")
    # 调用百度语音识别
    response = client.asr(get_file_content(msg.fileName), 'wav', 8000, {
        'lan': 'zh',
    })
    if response['err_no'] == 0:
        return response['result'][0]


def greetingToSnail():
    snailRobot.send("登陆成功", toUserName='filehelper')


def goodByeToSnail(message):
    if 'Bye' == message or '再见' == message:
        return True


@snailRobot.msg_register(itchat.content.ATTACHMENT)
def test_biaoqing(msg):
    print(msg)


@snailRobot.msg_register(itchat.content.TEXT, itchat.content.PICTURE)
def tell_my_love(msg):
    print(msg.user)
    author = snailRobot.search_friends(nickName='雯毓')[0]
    # 控制表白开始
    global POEMS
    if msg.user.UserName == 'filehelper':
        if msg.text == 'start':
            POEMS = { '0': "以下有三份我想对你说的话, 你选一个吧\r\n1:number version \r\n2:romantic version\r\n3:code version\r\n", '1': number_version, '2': romantic_version, '3': code_version}
            author.send(POEMS['0'])
            snailRobot.send("开始", toUserName='filehelper')
        if msg.text == 'stop':
            POEMS = {}
            snailRobot.send("暂停", toUserName='filehelper')

    poem = POEMS.get(msg.text, None)
    if poem is not None:
        if msg.user.UserName == 'filehelper' or msg.user.get('NickName') == '雯毓':
        #  if msg.user.UserName == 'filehelper' or msg.user.get('NickName') == '思是缘':
            if poem == "code_version":
                send_image(author)
            else:
                series_send_msg(author, poem)

            return "73 76 79 86 69 85"
            

@snailRobot.msg_register(itchat.content.VOICE)
def little_snail_reply(msg):
    print(msg.user)
    if msg.user.get('NickName') == '雯毓':
        message = voice_reply(msg)
        if message:
            if not goodByeToSnail(message):
                return text_reply(message)
            else:
                snailRobot.logout()


snailRobot.auto_login(hotReload=True, statusStorageDir='snailRobot.pkl', loginCallback=greetingToSnail)
snailRobot.run()
