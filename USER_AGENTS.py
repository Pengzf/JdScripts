#!/usr/bin/env python3
# -*- coding: utf-8 -*
'''
项目名称: JD-Script / USER_AGENTS
活动名称: User-agent
Author: SheYu09
'''
from time import time
from uuid import uuid4
from random import randint, uniform

def userAgent():
	ios = f'3.{randint(7, 8)}.{randint(0, 12)}'
	uuid = str(uuid4())
	iosVer = f'{randint(13, 14)}.{randint(0, 7)}.{randint(0, 2)}'
	iosV = iosVer.replace('.', '_')
	appBuild = randint(1088, 1129)
	return f"jdltapp;iPhone;{ios};{iosVer};{''.join(uuid.split('-'))};network/wifi;hasUPPay/0;pushNoticeIsOpen/1;lang/zh_CN;model/iPhone{randint(8, 13)},1;addressid/{int(uniform(1,2)*1e8)};hasOCPay/0;appBuild/{appBuild};supportBestPay/0;jdSupportDarkMode/0;pv/273.6;apprpd/;ref/JDLTSubMainPageViewController;psq/5;ads/;psn/{''.join(uuid.split('-'))}|{appBuild};jdv/0|iosapp|t_335139774|liteshare|Qqfriends|{int(time()*1e3)}|{int(time())+13};adk/;app_device/IOS;pap/JA2020_3112531|{ios}|IOS {iosVer};Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;"
	
	return f"jdltapp;iPhone;10.0.4;{iosVer};{''.join(uuid.split('-'))};network/wifi;ADID/{uuid.upper()};model/iPhone{randint(8, 13)},1;addressid/{int(uniform(1,2)*1e8)};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1"

