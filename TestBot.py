#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#远方的开发者，您好！这是一个XChat的测试机器人，使用Python编写。这里面提供了一些实例，供您参考！
import XChat    #引入模块
import time #引入模块

#信息接收处理函数，当有人在公屏上发送信息时，会调用这个。
#两个参数分别代表：信息内容和发送者。
def message_got(message,sender):
    print('收到 {who} 在公屏上发送的信息：{msg}'.format(who=sender,msg=message))

#用户加入处理函数，当有人加入当前聊天室，会调用这个。
#只有一个参数，这个参数代表昵称。
def user_join(nick):
    print("{user} 加入聊天室".format(user=nick))

#用户离开处理函数，当有人离开当前聊天室，会调用这个。
#只有一个参数，代表昵称。
def user_leave(nick):
    print("{user} 离开聊天室".format(user=nick))

#私信处理函数，当有人向客户端发送私信时，会调用这个。
#有两个参数，分别代表：私信内容和发送者。
def whisper_got(message,nick):
    print("{user} 向你发送了一条私信：{msg}".format(user=nick,msg=message))

#错误处理函数，当服务器告知客户端有错误时，将会调用这个。
def kill_errors(info):
    print("出错啦！详细信息：{}".format(info))
xc=XChat.XChat("dev","TestBot","TestBotPassword")  #实例化类，要提供三个参数，分别代表：聊天室名称、客户端昵称、可选密码。
xc.message_function+=[message_got]  #message_function 是一个列表，里面存放着信息处理函数。后面的以“_function”结尾的，都是如此。这个列表存放着信息接收函数。每个列表都可以添加多个函数。
xc.join_function+=[user_join]   #这个列表储存着用户加入处理函数。
xc.leave_function+=[user_leave] #这个列表存放着用户离开处理函数。
xc.whisper_function+=[whisper_got]  #这个列表存放着私信处理函数。
xc.error_function+=[kill_errors]    #这个列表存放错误处理函数。如果没有设置，将会使用库中自带的处理函数。建议添加自己的错误处理函数。
time.sleep(1)
xc.send_message("Hello World !")    #在公屏上发送信息
time.sleep(1)
xc.send_image("https://xq.kzw.ink/imgs/tx.png") #发送图片，只有一个参数，即图像地址
time.sleep(1)
print("图片字符串："+xc.get_image_text("https://xq.kzw.ink/imgs/tx.png")) #获取图片字符串，该字符串用来发送图片，参数只有一个，即图像地址
xc.send_big_message("大字测试","green") #使用LaTeX发送大字，第一个参数是内容，第二个参数是颜色，字符串类型，默认为红色。
#xc.send_to("目标","要发送的信息")   #发送私信，需要两个参数，分别是：目标、要发送的信息。
#xc.move("新的聊天室")   #该方法可以把自己移动到另一个聊天室。该方法过于简单，不做介绍。
#xc.change_nick("新的昵称")  #该方法可以修改自己的昵称，由于过于简单，所以不做介绍。
xc.run(False)    #该方法会不停地向服务器请求数据，接收信息，是个死循环。里面有一个参数，布尔值，如果为真，则直接给信息处理函数传递服务器返回的原数据；默认为假。注意：要开始接收信息，必须要有这一行代码！