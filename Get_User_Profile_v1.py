import requests;
import json;
import sys;
import os;

f = open ("data.txt", "w+", encoding = "utf-8");
headers = {"User-agent":"Mozilla/5.0"};

class GetUid (object):
    def __init__ (self):
        pass;
    def UN (self):
        url = "https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword=";
        username = input ("用户名: ");
        url += username;
        res = requests.get (url = url, headers = headers);
        res.encoding = "utf-8";
        data = json.loads (res.text);
        if (data["data"]["numResults"] == 0):
            print ("找不到此用户");
            f.close ();
            sys.exit (1);
        uid = str (data["data"]["result"][0]["mid"]);
        return uid;
    def ID (self):
        uid = input ("uid: ");
        return uid;

class GetData (object):
    def __init__ (self, uid):
        self.uid = uid;
    def BasicUserProfile (self):
        url = "https://api.bilibili.com/x/space/acc/info?mid=";
        url += self.uid;
        res = requests.get (url = url, headers = headers);
        res.encoding = "utf-8";
        data = json.loads (res.text);
        if (data["code"] != 0):
            print ("找不到此用户");
            f.close ();
            sys.exit (1);
        f.write ("用户名: " + data["data"]["name"] +", uid: " + str (data["data"]["mid"]) + ";\n");
    def AdvancedUserProfile (self):
        url = "https://api.bilibili.com/x/space/acc/info?mid=";
        url += self.uid;
        res = requests.get (url = url, headers = headers);
        res.encoding = "utf-8";
        data = json.loads (res.text);
        f.write ("\n用户信息:\n性别: " + data["data"]["sex"] + "\n等级: " + str (data["data"]["level"]) + "\n");
        if (data["data"]["vip"]["label"]["text"] == ""):
            f.write ("会员情况: 无会员\n");
        else:
            f.write ("会员情况: " + data["data"]["vip"]["label"]["text"] + "\n");
        if (data["data"]["sign"] != ""):
            f.write ("个性签名: " + data["data"]["sign"] + "\n");
        if (data["data"]["birthday"] != ""):
            f.write ("生日: " + data["data"]["birthday"] + "\n");
        print ("完成!");
    def bangumi (self):
        URL = "https://api.bilibili.com/x/space/bangumi/follow/list?type=1&vmid=";
        f.write ("\n追番列表:\n");
        pages = 0;
        records = 0;
        while (True):
            pages += 1;
            url = URL + self.uid + "&pn=" + str (pages);
            res = requests.get (url = url, headers = headers);
            res.encoding = "utf-8";
            data = json.loads (res.text);
            if (data["code"] == 53013):
                print ("用户隐私设置未公开");
                f.write("用户隐私设置未公开\n");
                break;
            if (len (data["data"]["list"]) == 0 and pages == 1):
                f.write ("无\n");
                break;
            for i in range (0, len (data["data"]["list"])):
                records += 1;
                f.write (str (records) + ". " + data["data"]["list"][i]["title"] + "\n");
            if (pages * 15 >= data["data"]["total"]):
                break;
        print ("完成!");
    def video (self):
        URL = "https://api.bilibili.com/x/space/arc/search?mid=";
        f.write ("\n视频列表:\n");
        pages = 0;
        records = 0;
        while (True):
            pages += 1;
            url = URL + self.uid + "&pn=" + str (pages);
            res = requests.get (url = url, headers = headers);
            res.encoding = "utf-8";
            data = json.loads (res.text);
            if (len (data["data"]["list"]["vlist"]) == 0 and pages == 1):
                f.write ("无\n");
                break;
            for i in range (0, len (data["data"]["list"]["vlist"])):
                records += 1;
                f.write (str (records) + ". " + data["data"]["list"]["vlist"][i]["title"] + "\n");
            if (pages * 30 >= data["data"]["page"]["count"]):
                break;
        print ("完成!");

op_input = GetUid ();
input_choice = input ("你想以哪种方式进行找到该用户?\n[1]用户名 [2]用户uid (受限于b站搜索机制, 使用用户名搜索的结果可能与预期不一致)\n");
if (input_choice == "1"):
    uid = op_input.UN ();
elif (input_choice == "2"):
    uid = op_input.ID ();
else:
    print ("输入的字符不能被识别");
    f.close ();
    sys.exit (1);

op_process = GetData (uid);
op_process.BasicUserProfile ();

while (True):
    data_choice = input ("你想要获取什么数据?\n[0]终止 [1]追番列表 [2]视频列表 [3]用户信息\n");
    if (data_choice == "0"):
        print ("完成! 已自动打开输出的txt文件 (位于同目录下的data.txt)\n");
        f.flush ();
        f.close ();
        os.system ("data.txt");
        sys.exit (0);
    elif (data_choice == "1"):
        op_process.bangumi ();
    elif (data_choice == "2"):
        op_process.video ();
    elif (data_choice == "3"):
        op_process.AdvancedUserProfile ();
    else:
        print ("输入的字符不能被识别");
