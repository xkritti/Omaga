# -*- coding: utf-8 -*-
from LineAPI.linepy import *
from LineAPI.akad.ttypes import Message
from LineAPI.akad.ttypes import ContentType as Type
from gtts import gTTS
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from googletrans import Translator
from humanfriendly import format_timespan, format_size, format_number, format_length
import time
import random
import sys
import json
import codecs
import threading
import glob
import re
import string
import os
import requests
import six
import ast
import pytz
import urllib
import urllib3
import urllib.parse
import traceback
import atexit
import json

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✯➣ พัฒนาโดย : http://github.com/xkrit.ti
✯➣ ไทย ( Thailand )
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
# first time login whit 4 PIN
# client = LINE("kk1.asian@gmail.com","casinokk1")
# copy authToken for bypass 4PIN in next time
# client = LINE("")
clientMid = client.profile.mid
clientProfile = client.getProfile()
clientSettings = client.getSettings()
clientPoll = OEPoll(client)
botStart = time.time()

msg_dict = {}
link_dict = {}
link_dict['ticket_sucess'] = []

settings = {
    "autoAdd": False,
    "autoJoin": True,
    "autoLeave": False,
    "autoRead": False,
    "autoRespon": False,
    "autoJoinTicket": True,
    "checkContact": False,
    "checkPost": False,
    "checkSticker": False,
    "changePictureProfile": False,
    "changeGroupPicture": [],
    "keyCommand": "",
    "myProfile": {
        "displayName": "",
        "coverId": "",
        "pictureStatus": "",
        "statusMessage": ""
    },
    "mimic": {
        "copy": False,
        "status": False,
        "target": {}
    },
    "setKey": False,
    "unsendMessage": False,
    "notified": True
}

read = {
    "ROM": {},
    "readPoint": {},
    "readMember": {},
    "readTime": {}
}

try:
    f = open('link.json',)
    # msg_dict = json.loads(f.read())
    data = json.load(f)
    temp_x = data['link']
    x = range(1006, len(temp_x))
    for i in x:
        data_loop = temp_x[i]
        temp_text = str(data_loop).split('/g/')
        print(i, temp_text[1])
        if settings["autoJoinTicket"] == True:
            print("ticket_id : ", temp_text[1])
            try:
                group = client.findGroupByTicket(temp_text[1])
                client.acceptGroupInvitationByTicket(group.id, temp_text[1])
                link_dict['ticket_sucess'].append({group.id})
                print("ได้เข้าร่วมกลุ่ม group %s" % str(group))
                client.sendMessage('c912cf7549762a0ac6d8cfe3b4f038f1d',
                                   "ได้เข้าร่วมกลุ่ม group %s" % str(group.name))
                time.sleep(60)

            except:
                print("can't join group !!!!")
                time.sleep(60)

    f.close()
except:
    print("Couldn't read Log data")

settings["myProfile"]["displayName"] = clientProfile.displayName
settings["myProfile"]["statusMessage"] = clientProfile.statusMessage
settings["myProfile"]["pictureStatus"] = clientProfile.pictureStatus
coverId = client.getProfileDetail()["result"]["objectId"]
settings["myProfile"]["coverId"] = coverId


def restartBot():
    print("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)


def shutdownBot():
    sys.exit("#============= BOT SHUTDOWN =============")


def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow, "(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday",
           "Wednesday", "Thursday", "Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
             "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]:
            hasil = day[i]
    for k in range(0, len(bulan)):
        if bln == str(k):
            bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(
        bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("logError.txt", "a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))


def cTime_to_datetime(unixtime):
    return datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))


def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')


def delete_log():
    ndt = datetime.now()
    for data in msg_dict:
        if (datetime.utcnow() - cTime_to_datetime(msg_dict[data]["createdTime"])) > timedelta(1):
            if "path" in msg_dict[data]:
                client.deleteFile(msg_dict[data]["path"])
            del msg_dict[data]


def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S': str(slen), 'E': str(elen - 4), 'M': mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S': str(slen), 'E': str(elen - 4), 'M': mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    client.sendMessage(to, textx, {'MENTION': str(
        '{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)


def command(text):
    pesan = text.lower()
    if settings["setKey"] == True:
        if pesan.startswith(settings["keyCommand"]):
            cmd = pesan.replace(settings["keyCommand"], "")
        else:
            cmd = "Undefined command"
    else:
        cmd = text.lower()
    return cmd


def helpmessage():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpMessage = "╔══[ Help Message ]" + "\n" + \
        "╠ " + key + "Help" + "\n" + \
        "╠══[ Status Command ]" + "\n" + \
        "╠ " + key + "Reboot" + "\n" + \
        "╠ " + key + "Shutdown" + "\n" + \
        "╠ " + key + "Runtime" + "\n" + \
        "╠ " + key + "Speed" + "\n" + \
        "╠ " + key + "Status" + "\n" + \
        "╠ MyKey" + "\n" + \
        "╠ SetKey「On/Off」" + "\n" + \
                    "╠══[ Settings Command ]" + "\n" + \
                    "╠ " + key + "AutoAdd「On/Off」" + "\n" + \
                    "╠ " + key + "AutoJoin「On/Off」" + "\n" + \
                    "╠ " + key + "AutoJoinTicket「On/Off」" + "\n" + \
                    "╠ " + key + "AutoLeave「On/Off」" + "\n" + \
                    "╠ " + key + "AutoRead「On/Off」" + "\n" + \
                    "╠ " + key + "AutoRespon「On/Off」" + "\n" + \
                    "╠ " + key + "CheckContact「On/Off」" + "\n" + \
                    "╠ " + key + "CheckPost「On/Off」" + "\n" + \
                    "╠ " + key + "CheckSticker「On/Off」" + "\n" + \
                    "╠ " + key + "UnsendChat「On/Off」" + "\n" + \
                    "╠══[ Self Command ]" + "\n" + \
                    "╠ " + key + "ChangeName:「ชื่อใหม่」" + "\n" + \
                    "╠ " + key + "ChangeBio:「ไบโอใหม่」" + "\n" + \
                    "╠ " + key + "Me" + "\n" + \
                    "╠ " + key + "MyMid" + "\n" + \
                    "╠ " + key + "MyName" + "\n" + \
                    "╠ " + key + "MyBio" + "\n" + \
                    "╠ " + key + "MyPicture" + "\n" + \
                    "╠ " + key + "MyVideoProfile" + "\n" + \
                    "╠ " + key + "MyCover" + "\n" + \
                    "╠ " + key + "StealContact「Mention」" + "\n" + \
                    "╠ " + key + "StealMid「Mention」" + "\n" + \
                    "╠ " + key + "StealName「Mention」" + "\n" + \
                    "╠ " + key + "StealBio「Mention」" + "\n" + \
                    "╠ " + key + "StealPicture「Mention」" + "\n" + \
                    "╠ " + key + "StealVideoProfile「Mention」" + "\n" + \
                    "╠ " + key + "StealCover「Mention」" + "\n" + \
                    "╠ " + key + "CloneProfile「Mention」" + "\n" + \
                    "╠ " + key + "RestoreProfile" + "\n" + \
                    "╠ " + key + "BackupProfile" + "\n" + \
                    "╠ " + key + "ChangePictureProfile" + "\n" + \
                    "╠══[ Group Command ]" + "\n" + \
                    "╠ " + key + "GroupCreator" + "\n" + \
                    "╠ " + key + "GroupId" + "\n" + \
                    "╠ " + key + "GroupName" + "\n" + \
                    "╠ " + key + "GroupPicture" + "\n" + \
                    "╠ " + key + "GroupTicket" + "\n" + \
                    "╠ " + key + "GroupTicket「On/Off」" + "\n" + \
                    "╠ " + key + "GroupList" + "\n" + \
                    "╠ " + key + "GroupMemberList" + "\n" + \
                    "╠ " + key + "GroupInfo" + "\n" + \
                    "╠ " + key + "ChangeGroupPicture" + "\n" + \
                    "╠══[ Special Command ]" + "\n" + \
                    "╠ " + key + "Mimic「On/Off」" + "\n" + \
                    "╠ " + key + "MimicList" + "\n" + \
                    "╠ " + key + "MimicAdd「Mention」" + "\n" + \
                    "╠ " + key + "MimicDel「Mention」" + "\n" + \
                    "╠ " + key + "Mention" + "\n" + \
                    "╠ " + key + "Lurking「On/Off/Reset」" + "\n" + \
                    "╠ " + key + "Lurking" + "\n" + \
                    "╠══[ Media Command ]" + "\n" + \
                    "╠ " + key + "InstaInfo 「UserName」" + "\n" + \
                    "╠ " + key + "SearchYoutube「Search」" + "\n" + \
                    "╚══[ Copyright @xkrit.ti ]"
    return helpMessage


def clientBot(op):
    try:
        if op.type == 0:
            print("[ 0 ] END OF OPERATION")
            return

        if op.type == 5:
            print("[ 5 ] NOTIFIED ADD CONTACT")
            if settings["autoAdd"] == True:
                client.findAndAddContactsByMid(op.param1)
            sendMention(
                op.param1, "Halo @!,terimakasih telah menambahkan saya sebagai teman :3")

        if op.type == 13:
            print("[ 13 ] NOTIFIED INVITE INTO GROUP")
            if clientMid in op.param3:
                if settings["autoJoin"] == True:
                    to = op.param1
                    client.acceptGroupInvitation(op.param1)
                    group = client.getGroup(to)
                    print("Gid : ", group.id, "\nGname : ",
                          group.name, "\nGmembers : ", group.members)

                # sendMention(op.param1, "Halo @!, Terimakasih Telah Mengundang Saya :3")

        if op.type == 15:
            print("[ 15 ] MEMBER LEAVE TO GROUP")
            if settings["notified"] == True:
                client.sendMessage(op.param1, "Bye Bye " +
                                   client.getContact(op.param2).displayName)

        if op.type == 17:
            print("[ 17 ] MEMBER JOIN TO GROUP")
            if settings["notified"] == True:
                client.sendMessage(op.param1, "ยินดีต้อนรับ " + client.getContact(op.param2).displayName +
                                   '\nแอดเพื่อน FoxTeam ก่อนสมัครเท่านั้น ' + '\n❗ถ้าแอดเพื่อนแล้วไม่ต้องแอดใหม่❗' + "\nhttps://lin.ee/jIGjdqe")

        if op.type in [22, 24]:
            print("[ 22 And 24 ] NOTIFIED INVITE INTO ROOM & NOTIFIED LEAVE ROOM")
            if settings["autoLeave"] == True:
                sendMention(op.param1, "Oi asw @!,c")
                client.leaveRoom(op.param1)

        if op.type == 25:
            try:
                print("[ 25 ] SEND MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                setKey = settings["keyCommand"].title()
                if settings["setKey"] == False:
                    setKey = ''
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if msg.contentType == 0:
                        if text is None:
                            return
                        else:
                            cmd = command(text)
                            if cmd == "help":
                                helpMessage = helpmessage()
                                client.sendMessage(to, str(helpMessage))
                            elif cmd.startswith("changekey:"):
                                sep = text.split(" ")
                                key = text.replace(sep[0] + " ", "")
                                if " " in key:
                                    client.sendMessage(
                                        to, "กรุณาใส่ Key")
                                else:
                                    settings["keyCommand"] = str(key).lower()
                                    client.sendMessage(
                                        to, "เปลี่ยนคีย์คำสั่งเป็น [ {} ]".format(str(key).lower()))
                            elif cmd == "speed":
                                start = time.time()
                                client.sendMessage(to, "Benchmarking...")
                                elapsed_time = time.time() - start
                                client.sendMessage(
                                    to, "[ Speed ]\nความเร็วในการส่งข้อความ {} วินาที".format(str(elapsed_time)))
                            elif cmd == "runtime":
                                timeNow = time.time()
                                runtime = timeNow - botStart
                                runtime = format_timespan(runtime)
                                client.sendMessage(
                                    to, "Bot ทำงานมา {}".format(str(runtime)))
                            elif cmd == "reboot":
                                client.sendMessage(
                                    to, "กำลังรีบูทบอท")
                                restartBot()
                            elif cmd == "shutdown":
                                client.sendMessage(
                                    to, "ออกจากระบบแล้ว ♪")
                                shutdownBot()
# Pembatas Script #
                            elif cmd == "noti on":
                                settings["notified"] = True
                                client.sendMessage(
                                    to, "เปิดการแจ้งเตือนแล้ว")
                            elif cmd == "noti off":
                                settings["notified"] = False
                                client.sendMessage(
                                    to, "ปิดการแจ้งเตือนแล้ว")
                            elif cmd == "autoadd on":
                                settings["autoAdd"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan auto add")
                            elif cmd == "autoadd off":
                                settings["autoAdd"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan auto add")
                            elif cmd == "autojoin on":
                                settings["autoJoin"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan auto join")
                            elif cmd == "autojoin off":
                                settings["autoJoin"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan auto join")
                            elif cmd == "autoleave on":
                                settings["autoLeave"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan auto leave")
                            elif cmd == "autoleave off":
                                settings["autoLeave"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan auto leave")
                            elif cmd == "autorespon on":
                                settings["autoRespon"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan auto respon")
                            elif cmd == "autorespon off":
                                settings["autoRespon"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan auto respon")
                            elif cmd == "autoread on":
                                settings["autoRead"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan auto read")
                            elif cmd == "autoread off":
                                settings["autoRead"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan auto read")
                            elif cmd == "autojointicket on":
                                settings["autoJoinTicket"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan auto join by ticket")
                            elif cmd == "autoJoinTicket off":
                                settings["autoJoin"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan auto join by ticket")
                            elif cmd == "checkcontact on":
                                settings["checkContact"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan check details contact")
                            elif cmd == "checkcontact off":
                                settings["checkContact"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan check details contact")
                            elif cmd == "checkpost on":
                                settings["checkPost"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan check details post")
                            elif cmd == "checkpost off":
                                settings["checkPost"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan check details post")
                            elif cmd == "checksticker on":
                                settings["checkSticker"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan check details sticker")
                            elif cmd == "checksticker off":
                                settings["checkSticker"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan check details sticker")
                            elif cmd == "unsendchat on":
                                settings["unsendMessage"] = True
                                client.sendMessage(
                                    to, "Berhasil mengaktifkan unsend message")
                            elif cmd == "unsendchat off":
                                settings["unsendMessage"] = False
                                client.sendMessage(
                                    to, "Berhasil menonaktifkan unsend message")
                            elif cmd == "status":
                                try:
                                    ret_ = "╔══[ Status ]"
                                    if settings["autoAdd"] == True:
                                        ret_ += "\n╠══[ ON ] Auto Add"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Auto Add"
                                    if settings["autoJoin"] == True:
                                        ret_ += "\n╠══[ ON ] Auto Join"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Auto Join"
                                    if settings["autoLeave"] == True:
                                        ret_ += "\n╠══[ ON ] Auto Leave Room"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Auto Leave Room"
                                    if settings["autoJoinTicket"] == True:
                                        ret_ += "\n╠══[ ON ] Auto Join Ticket"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Auto Join Ticket"
                                    if settings["autoRead"] == True:
                                        ret_ += "\n╠══[ ON ] Auto Read"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Auto Read"
                                    if settings["autoRespon"] == True:
                                        ret_ += "\n╠══[ ON ] Detect Mention"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Detect Mention"
                                    if settings["checkContact"] == True:
                                        ret_ += "\n╠══[ ON ] Check Contact"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Check Contact"
                                    if settings["checkPost"] == True:
                                        ret_ += "\n╠══[ ON ] Check Post"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Check Post"
                                    if settings["checkSticker"] == True:
                                        ret_ += "\n╠══[ ON ] Check Sticker"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Check Sticker"
                                    if settings["setKey"] == True:
                                        ret_ += "\n╠══[ ON ] Set Key"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Set Key"
                                    if settings["unsendMessage"] == True:
                                        ret_ += "\n╠══[ ON ] Unsend Message"
                                    else:
                                        ret_ += "\n╠══[ OFF ] Unsend Message"
                                    ret_ += "\n╚══[ Status ]"
                                    client.sendMessage(to, str(ret_))
                                except Exception as e:
                                    client.sendMessage(msg.to, str(e))
# Pembatas Script #
                            elif cmd == "crash":
                                client.sendContact(
                                    to, "u636ccaf511d2249875c8c4c66b6078b0")
                            elif cmd.startswith("changename:"):
                                sep = text.split(" ")
                                string = text.replace(sep[0] + " ", "")
                                if len(string) <= 20:
                                    profile = client.getProfile()
                                    profile.displayName = string
                                    client.updateProfile(profile)
                                    client.sendMessage(
                                        to, " เปลี่ยน display name เป็น +'\n'{}".format(str(string)))
                            elif cmd.startswith("changebio:"):
                                sep = text.split(" ")
                                string = text.replace(sep[0] + " ", "")
                                if len(string) <= 500:
                                    profile = client.getProfile()
                                    profile.statusMessage = string
                                    client.updateProfile(profile)
                                    client.sendMessage(
                                        to, "เปลี่ยน status message เป็น{}".format(str(string)))
                            elif cmd == "me":
                                sendMention(to, "@!", [sender])
                                client.sendContact(to, sender)
                            elif cmd == "mymid":
                                client.sendMessage(
                                    to, "[ MID ]\n{}".format(sender))
                            elif cmd == "myname":
                                contact = client.getContact(sender)
                                client.sendMessage(
                                    to, "[ Display Name ]\n{}".format(contact.displayName))
                            elif cmd == "mybio":
                                contact = client.getContact(sender)
                                client.sendMessage(
                                    to, "[ Status Message ]\n{}".format(contact.statusMessage))
                            elif cmd == "mypicture":
                                contact = client.getContact(sender)
                                client.sendImageWithURL(
                                    to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
                            elif cmd == "myvideoprofile":
                                contact = client.getContact(sender)
                                client.sendVideoWithURL(
                                    to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
                            elif cmd == "mycover":
                                channel = client.getProfileCoverURL(sender)
                                path = str(channel)
                                client.sendImageWithURL(to, path)
                            elif cmd.startswith("cloneprofile "):
                                if 'MENTION' in msg.contentMetadata.keys() != None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(
                                        msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        client.cloneContactProfile(ls)
                                        client.sendMessage(
                                            to, "Berhasil mengclone profile {}".format(contact.displayName))
                            elif cmd == "restoreprofile":
                                try:
                                    clientProfile = client.getProfile()
                                    clientProfile.displayName = str(
                                        settings["myProfile"]["displayName"])
                                    clientProfile.statusMessage = str(
                                        settings["myProfile"]["statusMessage"])
                                    clientProfile.pictureStatus = str(
                                        settings["myProfile"]["pictureStatus"])
                                    client.updateProfileAttribute(
                                        8, clientProfile.pictureStatus)
                                    client.updateProfile(clientProfile)
                                    coverId = str(
                                        settings["myProfile"]["coverId"])
                                    client.updateProfileCoverById(coverId)
                                    client.sendMessage(
                                        to, "Berhasil restore profile tunggu beberapa saat sampai profile berubah")
                                except Exception as e:
                                    client.sendMessage(
                                        to, "Gagal restore profile")
                                    logError(error)
                            elif cmd == "backupprofile":
                                try:
                                    profile = client.getProfile()
                                    settings["myProfile"]["displayName"] = str(
                                        profile.displayName)
                                    settings["myProfile"]["statusMessage"] = str(
                                        profile.statusMessage)
                                    settings["myProfile"]["pictureStatus"] = str(
                                        profile.pictureStatus)
                                    coverId = client.getProfileDetail()[
                                        "result"]["objectId"]
                                    settings["myProfile"]["coverId"] = str(
                                        coverId)
                                    client.sendMessage(
                                        to, "Berhasil backup profile")
                                except Exception as e:
                                    client.sendMessage(
                                        to, "Gagal backup profile")
                                    logError(error)
                            elif cmd.startswith("stealmid "):
                                if 'MENTION' in msg.contentMetadata.keys() != None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(
                                        msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    ret_ = "[ Mid User ]"
                                    for ls in lists:
                                        ret_ += "\n{}".format(str(ls))
                                    client.sendMessage(to, str(ret_))
                            elif cmd.startswith("stealname "):
                                if 'MENTION' in msg.contentMetadata.keys() != None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(
                                        msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        client.sendMessage(to, "[ Display Name ]\n{}".format(
                                            str(contact.displayName)))
                            elif cmd.startswith("stealbio "):
                                if 'MENTION' in msg.contentMetadata.keys() != None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(
                                        msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        client.sendMessage(to, "[ Status Message ]\n{}".format(
                                            str(contact.statusMessage)))
                            elif cmd.startswith("stealpicture"):
                                if 'MENTION' in msg.contentMetadata.keys() != None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(
                                        msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        path = "http://dl.profile.line.naver.jp/{}".format(
                                            contact.pictureStatus)
                                        client.sendImageWithURL(to, str(path))
                            elif cmd.startswith("stealvideoprofile "):
                                if 'MENTION' in msg.contentMetadata.keys() != None:
                                    names = re.findall(r'@(\w+)', text)
                                    mention = ast.literal_eval(
                                        msg.contentMetadata['MENTION'])
                                    mentionees = mention['MENTIONEES']
                                    lists = []
                                    for mention in mentionees:
                                        if mention["M"] not in lists:
                                            lists.append(mention["M"])
                                    for ls in lists:
                                        contact = client.getContact(ls)
                                        path = "http://dl.profile.line.naver.jp/{}/vp".format(
                                            contact.pictureStatus)
                                        client.sendVideoWithURL(to, str(path))
                            elif cmd.startswith("stealcover "):
                                if client != None:
                                    if 'MENTION' in msg.contentMetadata.keys() != None:
                                        names = re.findall(r'@(\w+)', text)
                                        mention = ast.literal_eval(
                                            msg.contentMetadata['MENTION'])
                                        mentionees = mention['MENTIONEES']
                                        lists = []
                                        for mention in mentionees:
                                            if mention["M"] not in lists:
                                                lists.append(mention["M"])
                                        for ls in lists:
                                            channel = client.getProfileCoverURL(
                                                ls)
                                            path = str(channel)
                                            client.sendImageWithURL(
                                                to, str(path))
# Pembatas Script #
                            elif cmd == 'joinbygid':
                                print('join by group id')
                                n = client.getGroupIdsJoined()
                                print(n)
                                # client.inviteIntoGroup('c912cf7549762a0ac6d8cfe3b4f038f1d','u83411c9d50d019047757c3f65e0a3061')
                            elif cmd == 'groupcreator':
                                group = client.getGroup(to)
                                GS = group.creator.mid
                                client.sendContact(to, GS)
                            elif cmd == 'groupid':
                                gid = client.getGroup(to)
                                client.sendMessage(
                                    to, "[ID Group : ]\n" + gid.id)
                            elif cmd == 'grouppicture':
                                group = client.getGroup(to)
                                path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                                client.sendImageWithURL(to, path)
                            elif cmd == 'groupname':
                                gid = client.getGroup(to)
                                client.sendMessage(
                                    to, "[Nama Group : ]\n" + gid.name)
                            elif cmd == 'groupticket':
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    if group.preventedJoinByTicket == False:
                                        # ot = "c912cf7549762a0ac6d8cfe3b4f038f1d"
                                        ticket = client.reissueGroupTicket(to)
                                        client.sendMessage(
                                            to, "[ Group Ticket ]\nhttps://line.me/R/ti/g/{}".format(str(ticket)))
                                    else:
                                        client.sendMessage(to, "Grup qr tidak terbuka silahkan buka terlebih dahulu dengan perintah {}openqr".format(
                                            str(settings["keyCommand"])))
                            elif cmd == 'groupticket on':
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    if group.preventedJoinByTicket == False:
                                        client.sendMessage(
                                            to, "Grup qr sudah terbuka")
                                    else:
                                        group.preventedJoinByTicket = False
                                        client.updateGroup(group)
                                        client.sendMessage(
                                            to, "Berhasil membuka grup qr")
                            elif cmd == 'groupticket off':
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    if group.preventedJoinByTicket == True:
                                        client.sendMessage(
                                            to, "Grup qr sudah tertutup")
                                    else:
                                        group.preventedJoinByTicket = True
                                        client.updateGroup(group)
                                        client.sendMessage(
                                            to, "Berhasil menutup grup qr")
                            elif cmd == 'groupinfo':
                                group = client.getGroup(to)
                                try:
                                    gCreator = group.creator.displayName
                                except:
                                    gCreator = "ไม่พบข้อมูล"
                                if group.invitee is None:
                                    gPending = "0"
                                else:
                                    gPending = str(len(group.invitee))
                                if group.preventedJoinByTicket == True:
                                    gQr = "เปิด"
                                    gTicket = "ไม่มี"
                                else:
                                    gQr = "เปิด"
                                    gTicket = "https://line.me/R/ti/g/{}".format(
                                        str(client.reissueGroupTicket(group.id)))
                                path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                                ret_ = "╔══[ Group Info ]"
                                ret_ += "\n╠ ชื่อกลุ่ม : {}".format(
                                    str(group.name))
                                ret_ += "\n╠ ID Group : {}".format(group.id)
                                ret_ += "\n╠ สร้างโดย : {}".format(
                                    str(gCreator))
                                ret_ += "\n╠ จำนวนสมาชิกทั้งหมด : {}".format(
                                    str(len(group.members)))
                                ret_ += "\n╠ จำนวนที่รอยืนยัน : {}".format(
                                    gPending)
                                ret_ += "\n╠ Group Qr : {}".format(gQr)
                                ret_ += "\n╠ Group Ticket : {}".format(gTicket)
                                ret_ += "\n╚══[ Finish ]"
                                client.sendMessage(to, str(ret_))
                                client.sendImageWithURL(to, path)
                            elif cmd == 'groupmemberlist':
                                if msg.toType == 2:
                                    group = client.getGroup(to)
                                    ret_ = "╔══[ Member List ]"
                                    no = 0 + 1
                                    for mem in group.members:
                                        ret_ += "\n╠ {}. {}".format(
                                            str(no), str(mem.displayName))
                                        no += 1
                                    ret_ += "\n╚══[ Total {} ]".format(
                                        str(len(group.members)))
                                    client.sendMessage(to, str(ret_))
                            elif cmd == 'grouplist':
                                groups = client.groups
                                ret_ = "╔══[ Group List ]"
                                no = 0 + 1
                                for gid in groups:
                                    group = client.getGroup(gid)
                                    ret_ += "\n╠ {}. {} | {}".format(
                                        str(no), str(group.name), str(len(group.members)))
                                    no += 1
                                ret_ += "\n╚══[ Total {} Groups ]".format(
                                    str(len(groups)))
                                client.sendMessage(to, str(ret_))
# Pembatas Script #
                            elif cmd == "เปลี่ยนรูปโปร":
                                settings["changePictureProfile"] = True
                                client.sendMessage(
                                    to, "กรุณาส่งภาพที่ต้องการเปลี่ยน")
                            elif cmd == "เปลี่ยนรูปกลุ่ม":
                                if msg.toType == 2:
                                    if to not in settings["changeGroupPicture"]:
                                        settings["changeGroupPicture"].append(
                                            to)
                                    client.sendMessage(
                                        to, "กรุณาส่งภาพที่ต้องการเปลี่ยน")
                            elif cmd == 'mention':
                                group = client.getGroup(msg.to)
                                nama = [
                                    contact.mid for contact in group.members]
                                k = len(nama)//100
                                for a in range(k+1):
                                    txt = u''
                                    s = 0
                                    b = []
                                    for i in group.members[a*100: (a+1)*100]:
                                        b.append(
                                            {"S": str(s), "E": str(s+6), "M": i.mid})
                                        s += 7
                                        txt += u'@xkrit.ti\n'
                                    client.sendMessage(to, text=txt, contentMetadata={
                                                       u'MENTION': json.dumps({'MENTIONEES': b})}, contentType=0)
                                    client.sendMessage(
                                        to, "Total {} Mention".format(str(len(nama))))
                            elif cmd == "lurking on":
                                tz = pytz.timezone("Asia/Bangkok")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday",
                                       "Wednesday", "Thursday", "Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa",
                                        "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                                         "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]:
                                        hasil = day[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k):
                                        bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime(
                                    '%Y') + "\n เวลา : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if receiver in read['readPoint']:
                                    try:
                                        del read['readPoint'][receiver]
                                        del read['readMember'][receiver]
                                        del read['readTime'][receiver]
                                    except:
                                        pass
                                    read['readPoint'][receiver] = msg_id
                                    read['readMember'][receiver] = ""
                                    read['readTime'][receiver] = readTime
                                    read['ROM'][receiver] = {}
                                    client.sendMessage(
                                        receiver, "Lurking telah diaktifkan")
                                else:
                                    try:
                                        del read['readPoint'][receiver]
                                        del read['readMember'][receiver]
                                        del read['readTime'][receiver]
                                    except:
                                        pass
                                    read['readPoint'][receiver] = msg_id
                                    read['readMember'][receiver] = ""
                                    read['readTime'][receiver] = readTime
                                    read['ROM'][receiver] = {}
                                    client.sendMessage(
                                        receiver, "Set reading point : \n" + readTime)
                            elif cmd == "lurking off":
                                tz = pytz.timezone("Asia/Bangkok")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday",
                                       "Wednesday", "Thursday", "Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa",
                                        "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                                         "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]:
                                        hasil = day[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k):
                                        bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime(
                                    '%Y') + "\nเวลา : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if receiver not in read['readPoint']:
                                    client.sendMessage(
                                        receiver, "Lurking ถูกปิดการใช้งาน")
                                else:
                                    try:
                                        del read['readPoint'][receiver]
                                        del read['readMember'][receiver]
                                        del read['readTime'][receiver]
                                    except:
                                        pass
                                    client.sendMessage(
                                        receiver, "Delete reading point : \n" + readTime)

                            elif cmd == "lurking reset":
                                tz = pytz.timezone("Asia/Bangkok")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday",
                                       "Wednesday", "Thursday", "Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa",
                                        "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                                         "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]:
                                        hasil = day[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k):
                                        bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime(
                                    '%Y') + "\nเวลา : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if msg.to in read["readPoint"]:
                                    try:
                                        del read["readPoint"][msg.to]
                                        del read["readMember"][msg.to]
                                        del read["readTime"][msg.to]
                                        del read["ROM"][msg.to]
                                    except:
                                        pass
                                    read['readPoint'][receiver] = msg_id
                                    read['readMember'][receiver] = ""
                                    read['readTime'][receiver] = readTime
                                    read['ROM'][receiver] = {}
                                    client.sendMessage(
                                        msg.to, "Reset reading point : \n" + readTime)
                                else:
                                    client.sendMessage(
                                        msg.to, "Lurking belum diaktifkan ngapain di reset?")

                            elif cmd == "lurking":
                                tz = pytz.timezone("Asia/Bangkok")
                                timeNow = datetime.now(tz=tz)
                                day = ["Sunday", "Monday", "Tuesday",
                                       "Wednesday", "Thursday", "Friday", "Saturday"]
                                hari = ["Minggu", "Senin", "Selasa",
                                        "Rabu", "Kamis", "Jumat", "Sabtu"]
                                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                                         "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                                hr = timeNow.strftime("%A")
                                bln = timeNow.strftime("%m")
                                for i in range(len(day)):
                                    if hr == day[i]:
                                        hasil = day[i]
                                for k in range(0, len(bulan)):
                                    if bln == str(k):
                                        bln = bulan[k-1]
                                readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime(
                                    '%Y') + "\nเวลา : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                                if receiver in read['readPoint']:
                                    if read["ROM"][receiver].items() == []:
                                        client.sendMessage(
                                            receiver, "Tidak Ada Sider")
                                    else:
                                        chiya = []
                                        for rom in read["ROM"][receiver].items():
                                            chiya.append(rom[1])
                                        cmem = client.getContacts(chiya)
                                        zx = ""
                                        zxc = ""
                                        zx2 = []
                                        xpesan = '[R E A D E R ]\n'
                                    for x in range(len(cmem)):
                                        xname = str(cmem[x].displayName)
                                        pesan = ''
                                        pesan2 = pesan+"@c\n"
                                        xlen = str(len(zxc)+len(xpesan))
                                        xlen2 = str(
                                            len(zxc)+len(pesan2)+len(xpesan)-1)
                                        zx = {'S': xlen, 'E': xlen2,
                                              'M': cmem[x].mid}
                                        zx2.append(zx)
                                        zxc += pesan2
                                    text = xpesan + zxc + "\n" + readTime
                                    try:
                                        client.sendMessage(receiver, text, contentMetadata={'MENTION': str(
                                            '{"MENTIONEES":'+json.dumps(zx2).replace(' ', '')+'}')}, contentType=0)
                                    except Exception as error:
                                        print(error)
                                    pass
                                else:
                                    client.sendMessage(
                                        receiver, "Lurking ไม่เปิดใช้งาน")
                            elif cmd.startswith("mimicadd"):
                                targets = []
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                for target in targets:
                                    try:
                                        settings["mimic"]["target"][target] = True
                                        client.sendMessage(
                                            msg.to, "Target ditambahkan!")
                                        break
                                    except:
                                        client.sendMessage(
                                            msg.to, "Gagal menambahkan target")
                                        break
                            elif cmd.startswith("mimicdel"):
                                targets = []
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                for target in targets:
                                    try:
                                        del settings["mimic"]["target"][target]
                                        client.sendMessage(
                                            msg.to, "Target dihapuskan!")
                                        break
                                    except:
                                        client.sendMessage(
                                            msg.to, "Gagal menghapus target")
                                        break

                            elif cmd == "mimiclist":
                                if settings["mimic"]["target"] == {}:
                                    client.sendMessage(
                                        msg.to, "Tidak Ada Target")
                                else:
                                    mc = "╔══[ Mimic List ]"
                                    for mi_d in settings["mimic"]["target"]:
                                        mc += "\n╠ " + \
                                            client.getContact(mi_d).displayName
                                    mc += "\n╚══[ Finish ]"
                                    client.sendMessage(msg.to, mc)

                            elif cmd.startswith("mimic"):
                                sep = text.split(" ")
                                mic = text.replace(sep[0] + " ", "")
                                if mic == "on":
                                    if settings["mimic"]["status"] == False:
                                        settings["mimic"]["status"] = True
                                        client.sendMessage(
                                            msg.to, "Reply Message on")
                                elif mic == "off":
                                    if settings["mimic"]["status"] == True:
                                        settings["mimic"]["status"] = False
                                        client.sendMessage(
                                            msg.to, "Reply Message off")
# Pembatas Script #
                            elif cmd.startswith("instainfo"):
                                try:
                                    sep = text.split(" ")
                                    search = text.replace(sep[0] + " ", "")
                                    r = requests.get(
                                        "https://www.instagram.com/{}/?__a=1".format(search))
                                    data = r.text
                                    data = json.loads(data)
                                    if data != []:
                                        ret_ = "╔══[ Profile Instagram ]"
                                        ret_ += "\n╠ Name : {}".format(
                                            str(data["graphql"]["user"]["full_name"]))
                                        ret_ += "\n╠ Username : {}".format(
                                            str(data["graphql"]["user"]["username"]))
                                        ret_ += "\n╠ Bio : {}".format(
                                            str(data["graphql"]["user"]["biography"]))
                                        ret_ += "\n╠ Follower : {}".format(
                                            str(data["graphql"]["user"]["edge_followed_by"]["count"]))
                                        ret_ += "\n╠ Following : {}".format(
                                            str(data["graphql"]["user"]["edge_follow"]["count"]))
                                        if data["graphql"]["user"]["is_verified"] == True:
                                            ret_ += "\n╠ Verify : Yes"
                                        else:
                                            ret_ += "\n╠ Verify : No"
                                        if data["graphql"]["user"]["is_private"] == True:
                                            ret_ += "\n╠ Private Account : Yes"
                                        else:
                                            ret_ += "\n╠ Private Account : No"
                                        ret_ += "\n╠ Total Post : {}".format(
                                            str(data["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]))
                                        ret_ += "\n╚══[ https://www.instagram.com/{} ]".format(
                                            search)
                                        path = data["graphql"]["user"]["profile_pic_url_hd"]
                                        client.sendImageWithURL(to, str(path))
                                        client.sendMessage(to, str(ret_))
                                except Exception as error:
                                    logError(error)

                            elif cmd.startswith("searchyoutube"):
                                sep = text.split(" ")
                                search = text.replace(sep[0] + " ", "")
                                params = {"search_query": search}
                                r = requests.get(
                                    "https://www.youtube.com/results", params=params)
                                soup = BeautifulSoup(r.content, "html5lib")
                                ret_ = "╔══[ Youtube Result ]"
                                datas = []
                                for data in soup.select(".yt-lockup-title > a[title]"):
                                    if "&lists" not in data["href"]:
                                        datas.append(data)
                                for data in datas:
                                    ret_ += "\n╠══[ {} ]".format(
                                        str(data["title"]))
                                    ret_ += "\n╠ https://www.youtube.com{}".format(
                                        str(data["href"]))
                                ret_ += "\n╚══[ Total {} ]".format(len(datas))
                                client.sendMessage(to, str(ret_))
# Pembatas Script #
                        if text.lower() == "mykey":
                            client.sendMessage(to, "KeyCommand ตอนนี้คือ [ {} ]".format(
                                str(settings["keyCommand"])))
                        elif text.lower() == "setkey on":
                            settings["setKey"] = True
                            client.sendMessage(
                                to, "setkey เปิดการใช้งานเรียบร้อย ")
                        elif text.lower() == "setkey off":
                            settings["setKey"] = False
                            client.sendMessage(
                                to, "setkey ปิดการใช้งานเรียบร้อย")
# Pembatas Script #
                    elif msg.contentType == 1:
                        if settings["changePictureProfile"] == True:
                            path = client.downloadObjectMsg(msg_id)
                            settings["changePictureProfile"] = False
                            client.updateProfilePicture(path)
                            client.sendMessage(
                                to, "เปลี่ยนรูปโปรไฟล์สำเร็จแล้ว")
                        if msg.toType == 2:
                            if to in settings["changeGroupPicture"]:
                                path = client.downloadObjectMsg(msg_id)
                                settings["changeGroupPicture"].remove(to)
                                client.updateGroupPicture(to, path)
                                client.sendMessage(
                                    to, "เปลี่ยนรูปโปรไฟล์กลุ่มสำเร็จแล้ว")
                    elif msg.contentType == 7:
                        if settings["checkSticker"] == True:
                            stk_id = msg.contentMetadata['STKID']
                            stk_ver = msg.contentMetadata['STKVER']
                            pkg_id = msg.contentMetadata['STKPKGID']
                            ret_ = "╔══[ Sticker Info ]"
                            ret_ += "\n╠ STICKER ID : {}".format(stk_id)
                            ret_ += "\n╠ STICKER PACKAGES ID : {}".format(
                                pkg_id)
                            ret_ += "\n╠ STICKER VERSION : {}".format(stk_ver)
                            ret_ += "\n╠ STICKER URL : line://shop/detail/{}".format(
                                pkg_id)
                            ret_ += "\n╚══[ Finish ]"
                            client.sendMessage(to, str(ret_))
                    elif msg.contentType == 13:
                        if settings["checkContact"] == True:
                            try:
                                contact = client.getContact(
                                    msg.contentMetadata["mid"])
                                if client != None:
                                    cover = client.getProfileCoverURL(
                                        msg.contentMetadata["mid"])
                                else:
                                    cover = "ไม่สามารถเข้า line channel"
                                path = "http://dl.profile.line-cdn.net/{}".format(
                                    str(contact.pictureStatus))
                                try:
                                    client.sendImageWithURL(to, str(path))
                                except:
                                    pass
                                ret_ = "╔══[ Details Contact ]"
                                ret_ += "\n╠ Nama : {}".format(
                                    str(contact.displayName))
                                ret_ += "\n╠ MID : {}".format(
                                    str(msg.contentMetadata["mid"]))
                                ret_ += "\n╠ Bio : {}".format(
                                    str(contact.statusMessage))
                                ret_ += "\n╠ Gambar Profile : http://dl.profile.line-cdn.net/{}".format(
                                    str(contact.pictureStatus))
                                ret_ += "\n╠ Gambar Cover : {}".format(
                                    str(cover))
                                ret_ += "\n╚══[ Finish ]"
                                client.sendMessage(to, str(ret_))
                            except:
                                client.sendMessage(to, "Contact error")
                    elif msg.contentType == 16:
                        if settings["checkPost"] == True:
                            try:
                                ret_ = "╔══[ Details Post ]"
                                if msg.contentMetadata["serviceType"] == "GB":
                                    contact = client.getContact(sender)
                                    auth = "\n╠ Penulis : {}".format(
                                        str(contact.displayName))
                                else:
                                    auth = "\n╠ Penulis : {}".format(
                                        str(msg.contentMetadata["serviceName"]))
                                purl = "\n╠ URL : {}".format(
                                    str(msg.contentMetadata["postEndUrl"]).replace("line://", "https://line.me/R/"))
                                ret_ += auth
                                ret_ += purl
                                if "mediaOid" in msg.contentMetadata:
                                    object_ = msg.contentMetadata["mediaOid"].replace(
                                        "svc=myhome|sid=h|", "")
                                    if msg.contentMetadata["mediaType"] == "V":
                                        if msg.contentMetadata["serviceType"] == "GB":
                                            ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(
                                                str(msg.contentMetadata["mediaOid"]))
                                            murl = "\n╠ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(
                                                str(msg.contentMetadata["mediaOid"]))
                                        else:
                                            ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(
                                                str(object_))
                                            murl = "\n╠ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(
                                                str(object_))
                                        ret_ += murl
                                    else:
                                        if msg.contentMetadata["serviceType"] == "GB":
                                            ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(
                                                str(msg.contentMetadata["mediaOid"]))
                                        else:
                                            ourl = "\n╠ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(
                                                str(object_))
                                    ret_ += ourl
                                if "stickerId" in msg.contentMetadata:
                                    stck = "\n╠ Stiker : https://line.me/R/shop/detail/{}".format(
                                        str(msg.contentMetadata["packageId"]))
                                    ret_ += stck
                                if "text" in msg.contentMetadata:
                                    text = "\n╠ Tulisan : {}".format(
                                        str(msg.contentMetadata["text"]))
                                    ret_ += text
                                ret_ += "\n╚══[ Finish ]"
                                client.sendMessage(to, str(ret_))
                            except:
                                client.sendMessage(to, "Post error")
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)

        if op.type == 26:
            try:
                print("[ 26 ] RECIEVE MESSAGE")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if settings["autoRead"] == True:
                        client.sendChatChecked(to, msg_id)
                    if to in read["readPoint"]:
                        if sender not in read["ROM"][to]:
                            read["ROM"][to][sender] = True
                    if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                        text = msg.text
                        if text is not None:
                            client.sendMessage(msg.to, text)
                    if settings["unsendMessage"] == True:
                        try:
                            msg = op.message
                            if msg.toType == 0:
                                client.log("[{} : {}]".format(
                                    str(msg._from), str(msg.text)))
                            else:
                                client.log("[{} : {}]".format(
                                    str(msg.to), str(msg.text)))
                                msg_dict[msg.id] = {"text": msg.text, "from": msg._from, "createdTime": msg.createdTime,
                                                    "contentType": msg.contentType, "contentMetadata": msg.contentMetadata}
                        except Exception as error:
                            logError(error)
                    if msg.contentType == 0:
                        if text is None:
                            return
                        if "/ti/g/" in msg.text.lower():
                            if settings["autoJoinTicket"] == True:
                                link_re = re.compile(
                                    '(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                                links = link_re.findall(text)
                                n_links = []
                                for l in links:
                                    if l not in n_links:
                                        n_links.append(l)
                                print(n_links)
                                for ticket_id in n_links:
                                    print("ticket_id : ", ticket_id)
                                    group = client.findGroupByTicket(ticket_id)
                                    client.acceptGroupInvitationByTicket(
                                        group.id, ticket_id)
                                    print("ได้เข้าร่วมกลุ่ม group %s" %
                                          str(group))
                                    # client.sendMessage(
                                    #     to, "ได้เข้าร่วมกลุ่ม group %s" % str(group.name))
                        if 'MENTION' in msg.contentMetadata.keys() != None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(
                                msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if clientMid in mention["M"]:
                                    if settings["autoRespon"] == True:
                                        sendMention(
                                            sender, "Oi Asw @!,jangan main tag tag", [sender])
                                    break
                        if 'export' == msg.text:
                            with open('data.txt', "w") as outfile:
                                json.dump(link_dict, outfile)

            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
        if op.type == 65:
            print("[ 65 ] NOTIFIED DESTROY MESSAGE")
            if settings["unsendMessage"] == True:
                try:
                    at = op.param1
                    msg_id = op.param2
                    if msg_id in msg_dict:
                        if msg_dict[msg_id]["from"]:
                            contact = client.getContact(
                                msg_dict[msg_id]["from"])
                            if contact.displayNameOverridden != None:
                                name_ = contact.displayNameOverridden
                            else:
                                name_ = contact.displayName
                                ret_ = "Send Message cancelled."
                                ret_ += "\nSender : @!"
                                ret_ += "\nSend At : {}".format(
                                    str(dt_to_str(cTime_to_datetime(msg_dict[msg_id]["createdTime"]))))
                                ret_ += "\nType : {}".format(
                                    str(Type._VALUES_TO_NAMES[msg_dict[msg_id]["contentType"]]))
                                ret_ += "\nText : {}".format(
                                    str(msg_dict[msg_id]["text"]))
                                sendMention(at, str(ret_), [contact.mid])
                            del msg_dict[msg_id]
                        else:
                            client.sendMessage(
                                at, "SentMessage cancelled,But I didn't have log data.\nSorry > <")
                except Exception as error:
                    logError(error)
                    traceback.print_tb(error.__traceback__)

        if op.type == 55:
            print("[ 55 ] NOTIFIED READ MESSAGE")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                else:
                    pass
            except Exception as error:
                logError(error)
                traceback.print_tb(error.__traceback__)
    except Exception as error:
        logError(error)
        traceback.print_tb(error.__traceback__)


while True:
    try:
        delete_log()
        ops = clientPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clientBot(op)
                clientPoll.setRevision(op.revision)
    except Exception as error:
        logError(error)


def atend():
    print("Saving")
    with open("Log_data.json", "w", encoding='utf8') as f:
        json.dump(msg_dict, f, ensure_ascii=False,
                  indent=4, separators=(',', ': '))
    print("BYE")


atexit.register(atend)
