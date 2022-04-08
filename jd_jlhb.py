#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_jlhb
活动名称: 锦鲤红包-助力
Author: SheYu09
cron: 0 0 * * * jd_jlhb.py
new Env('京东 -*- 锦鲤红包')
'''
import requests, os
s = requests.session()
SheYu09 = 'https://raw.gh.fakev.cn/SheYu09/JdScripts/main/'
try: from GetJDUser import *
except: os.system(f'wget {SheYu09}GetJDUser.so')
requests.packages.urllib3.disable_warnings()

def pop_ck():
	while len(Names)+1 <= len(ckList): ckList.pop()

def JD_API_PARAMS():
	s.params = {
		'appid': 'jinlihongbao',
		'functionId': '',
		'loginType': 2,
		'client': 'jinlihongbao',
		't': '',
		'clientVersion': '10.4.6',
		'osVersion': -1,
		'body': {}
	}
	s.params['t'] = int(time()*1e3)
	s.headers['Referer'] = 'https://happy.m.jd.com/'

def JD_API_BODY():
	s.body = {
		'random': '',
		'log': '',
		'sceneid': 'JLHBhPageh5'
	}

def JD_API_HOST():
	r = s.post('https://api.m.jd.com/api', verify=False); return r.text if r.content else '' 

def h5launch():
	global h5launchinfo
	s.params['functionId'] = stack()[0][3]
	s.body['followShop'] = 0
	s.params['body'] = dumps(s.body, separators=(',', ':'))
	h5launchinfo = JD_API_HOST()
	return h5launchinfo

def h5activityIndex():
	global h5activity
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps({
		"isjdapp": 1
	}, separators=(',', ':'))
	h5activity = JD_API_HOST()

def h5assist():
	global h5assistinfo
	s.params['functionId'] = 'jinli_' + stack()[0][3]
	s.body['redPacketId'] = redPacketId
	s.body['followShop'] = 0
	s.params['body'] = dumps(s.body, separators=(',', ':'))
	h5assistinfo = JD_API_HOST()

def h5receiveRedpacketAll(e):
	global h5receive
	s.params['functionId'] = stack()[0][3]
	if e:
		s.body['taskType'] = taskType
	s.params['body'] = dumps(s.body, separators=(',', ':'))
	h5receive = JD_API_HOST()

def taskHomePage():
	global taskHome
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = {}
	taskHome = JD_API_HOST()

def startTask():
	global startTaskinfo
	s.params['functionId'] = stack()[0][3]
	s.body['taskType'] = taskType
	s.params['body'] = dumps(s.body, separators=(',', ':'))
	startTaskinfo = JD_API_HOST()

def getTaskDetailForColor():
	global getTaskDetail
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps({
		'taskType': taskType
	}, separators=(',', ':'))
	getTaskDetail = JD_API_HOST()

def taskReportForColor():
	global taskReport
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps({
		'taskType': taskType,
		'detailId': detailId
	}, separators=(',', ':'))
	taskReport = JD_API_HOST()

def BoostCode(i):
	JD_API_BODY(); s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"开始【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n"); JD_API_PARAMS(); h5activityIndex()
	if compile(r'"hasAssistNum":(.*?),').findall(h5activity)[::-1][0] == findall("\d+", compile(r'"requireAssistNum":(.*?),').findall(h5activity)[::-1][0])[0]: print("啊偶，TA的助力已满，开启自己的红包活动吧~\n"); return
	redPacketId = re_key('"id":(.*?),', h5activity) if re_key('"id":(.*?),', h5activity) else re_key('"id":(.*?),', h5launch())
	print(f"【京东账号{ckList.index(i)+1}（{s.nickName}）的锦鲤红包好友互助码】{redPacketId}\n")
	redPacketIdList.append(redPacketId); sleep(s.t)

def jdkoi(i):
	global redPacketId
	JD_API_BODY(); s.headers['Cookie'] = i
	if GetJDUser(): return
	JD_API_PARAMS(); redPacketId = redPacketIdList[0]; print(f"【用户{ckList.index(i)+1}（{s.nickName}）助力】{redPacketId}\n"); h5assist(); statusDesc = re_key('"statusDesc":"(.*?)"', h5assistinfo)
	(statusDesc and [print(statusDesc, "\n")] or [print(h5assistinfo, "\n")])[0]; statusDesc and 'TA的助力已满' in statusDesc and len(redPacketIdList) == 1 and pop_ck() or redPacketIdList.remove(redPacketId) if statusDesc and 'TA的助力已满' in statusDesc else ''
	if re_key('"rtn_code":(.*?),', h5assistinfo) == '403': s.t += 1; print(s.t)
	sleep(s.t)

def Redenvelopes(i):
	JD_API_BODY(); s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"开始【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n"); JD_API_PARAMS(); h5activityIndex()
	msg = re_key('"msg":(.*?),', h5activity)
	if '限制' in msg: print("已达拆红包数量限制\n"); return
	for i in range(8):
		h5receiveRedpacketAll(''); biz_msg = re_key('"biz_msg":"(.*?)"', h5receive); sleep(s.t)
		try: 
			if '次数已用光' in biz_msg or '还未发起' in biz_msg: print(biz_msg, "\n"); break
			discount = re_key('"discount":"(.*?)"', h5receive); print(f"{biz_msg}: {discount}元\n")
		except: print(h5receive, "\n"); break

def Doatask():
	JD_API_BODY(); s.headers['Cookie'] = i
	if GetJDUser(): return
	print(f"开始【京东账号{ckList.index(i)+1}】{s.userLevel}级 {s.levelName}: {s.nickName}\n"); JD_API_PARAMS(); taskHomePage()
	for i in loads(re_key('"taskInfos":(\[.*?\]),', taskHome), strict=False):
		title = i['title']; taskType = i['taskType']
		if '券' in title: continue
		print(f"开始: {title}\n")
		if i['alreadyReceivedCount'] == i['requireCount']: h5receiveRedpacketAll('e') if i['innerStatus'] == 3 else print("任务已结束(领取过红包)\n")
		else: continue

def start():
	global Names, ckList, redPacketIdList; print("🔔锦鲤红包, 开始!\n"); 
	Names = Name()
	ckList = jdCookie(); redPacketIdList = list(); s.name = split('[_.]', os.path.basename(__file__)); s.t = 60
	[BoostCode(i) for i in [i for i in ckList if re_pin(i) in Names]]
	redPacketIdList and [jdkoi(i) for i in ckList]
	[Redenvelopes(i) for i in [i for i in ckList if re_pin(i) in Names]]

if __name__ == '__main__':
	start()
