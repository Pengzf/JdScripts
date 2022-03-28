#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / jd_tyt
活动名称: 发财挖宝
Author: SheYu09
cron: 0 0 * * * jd_tyt.py
new Env('极速版 -*- 发财挖宝')
'''
import requests
s = requests.session()
SheYu09 = 'https://raw.fastgit.org/SheYu09/JdScripts/main/'
try:
	from h5st import h5st
except:
	os.system(f'wget {SheYu09}h5st.so')
from re import compile
from inspect import stack
from time import sleep, time
from json import dumps, loads
from GetJDUser import GetJDUser
try:
	from GetJDUser import GetJDUser
except:
	os.system(f'wget {SheYu09}GetJDUser.so')
requests.packages.urllib3.disable_warnings()
s.params = {
	'functionId': '',
	'body': '',
	't': '',
	'appid': 'activities_platform',
	'client': 'H5',
	'clientVersion': '1.0.0'
}
s.headers['Referer'] = 'https://bnzf.jd.com/'

def re_pin(r):
	try:
		return compile(r'pin=(.*?);wskey=.*?;').findall(r)[0]
	except:
		try:
			return compile(r'pt_key=.*?;pt_pin=(.*?);').findall(r)[0]
		except:
			print(r, '\nck格式不正确，请检查\n')

def re_key(r, e):
	try:
		return compile(rf'{r}').findall(e)[::-1][0]
	except:
		pass

def JD_API_BODY():
	global body
	body = {
		'linkId': 'pTTvJeSTrpthgk9ASBVGsw'
	}

def JD_API_HOST():
	s.headers['User-Agent'] = userAgent()
	r = s.get('https://api.m.jd.com/', verify=False)
	return r.text if r.content else ''

def happyDigHome():
	global s, DigHomeinfo
	s.params['functionId'] = stack()[0][3]
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['t'] = int(time()*1e3)
	s = h5st(s, 'ce6c2')
	DigHomeinfo = JD_API_HOST()

def happyDigDo(round, rowIdx, colIdx):
	global DigDoinfo
	JD_API_BODY()
	s.params['functionId'] = stack()[0][3]
	body['round'] = round
	body['rowIdx'] = rowIdx
	body['colIdx'] = colIdx
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['t'] = int(time()*1e3)
	DigDoinfo = JD_API_HOST()

def happyDigHelpList():
	global DigHelpListinfo
	JD_API_BODY()
	s.params['functionId'] = stack()[0][3]
	body['pageNum'] = 1
	body['pageSize'] = 50
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['t'] = int(time()*1e3)
	DigHelpListinfo = JD_API_HOST()

def happyDigHelp(inviter, inviteCode):
	global s, DigHelpinfo
	JD_API_BODY()
	s.params['functionId'] = stack()[0][3]
	body['inviter'] = inviter
	body['inviteCode'] = inviteCode
	s.params['body'] = dumps(body, separators=(',', ':'))
	s.params['t'] = int(time()*1e3)
	s = h5st(s, '8dd95')
	DigHelpinfo = JD_API_HOST()

def BoostCode(i):
	global body
	s.headers['Cookie'] = i; ck, levelName, nickName, userLevel = GetJDUser(s)
	if not ck: return
	s.headers['Cookie'] = ck; 
	print(f"开始【京东账号{ckList.index(i)+1}】{userLevel}级 {levelName}: {nickName}\n"); JD_API_BODY(); happyDigHome(); DigTreasure(ck); happyDigHelpList(); inviter = re_key('"markedPin":"(.*?)"', DigHomeinfo); inviteCode = re_key('"inviteCode":"(.*?)"', DigHomeinfo); personNum = int(re_key('"personNum":(.*?),', DigHelpListinfo)); inviterList.append(inviter); inviteCodeList.append(inviteCode); personNumList.append(personNum)
	print(f"inviter: {inviter}\ninviteCode: {inviteCode}\n邀请人数: {personNum}\n")

def HelpFriends(i):
	for inviter, inviteCode, personNum in zip(inviterList, inviteCodeList, personNumList):
		if personNumList[0] >= 40: inviterList.remove(inviter); inviteCodeList.remove(inviteCode); personNumList.pop(0); sleep(2); continue
		s.headers['Cookie'] = i; ck, levelName, nickName, userLevel = GetJDUser(s)
		if not ck: break
		s.headers['Cookie'] = ck; print(f"【用户{ckList.index(i)+1}（{nickName}）助力】{inviter}\n"); happyDigHelp(inviter, inviteCode); errMsg = re_key('"errMsg":"(.*?)"', DigHelpinfo); print(errMsg, "\n")
		if errMsg == 'success':
			personNumList[0] += 1
			print(f"邀请人数: {personNum+1}\n")
		sleep(2); break

def DigTreasure(i):
	s.headers['Cookie'] = i; ck, levelName, nickName, userLevel = GetJDUser(s)
	if not ck: return
	s.headers['Cookie'] = ck; print(f"开始挖宝【京东账号{ckList.index(i)+1}】{userLevel}级 {levelName}: {nickName}\n")
	break_info = False
	for round in range(3):
		JD_API_BODY()
		body['round'] = round+1
		happyDigHome()
		DigHome = loads(re_key('"roundList":(\[.*?\]),', DigHomeinfo), strict=False)[round]
		if DigHome['state'] != 0: continue
		for i in DigHome['chunks']:
			if i['type']: continue
			happyDigDo(round+1, i['rowIdx'], i['colIdx'])
			errMsg = re_key('"errMsg":"(.*?)"', DigDoinfo)
			print(errMsg, "\n")
			if '生命值' in errMsg: break_info = True; break
			type = re_key('"type":(.*?),', DigDoinfo)
			value = re_key('"value":"(.*?)"', DigDoinfo) if type != '4' else '💣'
			type = type == '1' and '优惠卷' or type == '2' and '京东红包' or type == '3' and '微信红包' or type == '4' and '炸弹'
			print(f"挖到{type}: {value}\n")
			sleep(3)
		if break_info:
			break

def start():
	global ckList, inviterList, inviteCodeList, personNumList; print("🔔发财挖宝, 开始!\n"); inviterList, inviteCodeList, personNumList = list(), list(), list(); ckList = jdCookie(); 
	'''[BoostCode(c) for c in [c for c in ckList if re_pin(c) in Name()]]
	inviterList and inviteCodeList and [HelpFriends(c) for c in ckList]
	print(inviterList, personNumList)
	inviterList and inviteCodeList and [HelpFriends(c) for c in ckList]'''
	[DigTreasure(c) for c in [c for c in ckList if re_pin(c) in Name()]]

if __name__ == '__main__':
	start()
