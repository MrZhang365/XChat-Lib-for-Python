import json
import threading
import time
import websocket
import ssl
class XChat:    #一个类
    userset=False
    def __init__(self,token,channel,nick,password="",headurl="https://xq.kzw.ink/imgs/tx.png"):
        self.channel = channel
        self.nick = nick
        self.password=password
        self.token=token
        self.head_url=headurl
        self.online_users = []
        self.message_function = []
        self.whisper_function = []
        self.join_function = []
        self.leave_function = []
        self.error_function = []
        self.ws = websocket.create_connection("wss://xq.kzw.ink/ws",sslopt={"cert_reqs": ssl.CERT_NONE})
        self.send_packet({"cmd": "join", "channel": channel, "nick": nick,"password":password,"token":token})
        threading.Thread(target=self.ping_thread).start()
    def send_message(self, msg,show=False):
        if show:
            self.send_packet({"cmd": "chat", "text": msg,"head":self.head_url,"show":"1"})
        else:
            self.send_packet({"cmd": "chat", "text": msg,"head":self.head_url})
    def send_to(self, target, msg):
        self.send_packet({"cmd": "whisper", "nick": target, "text": msg})
    def move(self, new_channel):
        self.channel = new_channel
        self.send_packet({"cmd": "move", "channel": new_channel})
    def change_nick(self, new_nick):
        self.nick = new_nick
        self.send_packet({"cmd": "changenick", "nick": new_nick})
    def send_packet(self, packet):
        encoded = json.dumps(packet)
        self.ws.send(encoded)
    def daemon(self):
        self.daemon_thread=threading.Thread(target=self.run)
        self.daemon_thread.start()
    def send_image(self,image_url,image_name="Image"):
        self.send_message("[![{img_name}]({img_url})]({img_url})".format(img_name=image_name,img_url=image_url))
    def get_image_text(self,image_url,image_name="Image"):
        return("[![{img_name}]({img_url})]({img_url})".format(img_name=image_name,img_url=image_url))
    def run(self,return_more=False):
        while True:
            result = json.loads(self.ws.recv())
            if result["cmd"] == "chat" and not result["nick"] == self.nick:
                for function in list(self.message_function):
                    if return_more==False:
                        function(result["text"], result["nick"])
                    else:
                        function(result)
            elif result["cmd"] == "onlineAdd":
                self.online_users.append(result["nick"])
                for function in list(self.join_function):
                    if return_more==False:
                        function(result["nick"])
                    else:
                        function(result)
            elif result["cmd"] == "onlineRemove":
                self.online_users.remove(result["nick"])
                for function in list(self.leave_function):
                    if return_more==False:
                        function(result["nick"])
                    else:
                        function(result)
            elif result["cmd"] == "onlineSet":
                for nick in result["nicks"]:
                    self.online_users.append(nick)
            elif result["cmd"] == "info" and result.get("type") == "whisper":
                for function in list(self.whisper_function):
                    if return_more==False:
                        if "from" in result:function(result["text"][len(result["from"])+12:],result["from"])
                    else:
                        function(result)
            elif result["cmd"]=="warn":
                if len(self.error_function)==0:
                    print("\a服务器向客户端报告了错误！内容："+result["text"]+"\n代码还在继续运行，请尽快处理！！！")
                else:
                    for function in list(self.error_function):
                        if not return_more:
                            function(result["text"])
                        else:
                            function(result)
    def ping_thread(self):
        while self.ws.connected:
            self.send_packet({"cmd": "ping"})
            time.sleep(60)
if __name__=="__main__":
    print("不好意思，这只是一个库，不能单独运行呦。")
    input("请按下 Enter 键退出")
#好的程序，都是改出来的，如果发现这个库有BUG，请及时联系我！
#我的邮箱：
#3288492688@qq.com
#Xiao_Zhang_123@outlook.com
