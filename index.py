# coding: utf-8
'''
@author: FreezingTiny
@contact: i@fsql.net
@desc: 腾讯视频好莱坞会员V力值签到，一次正常签到，一次手机签到，同时尝试4个任务领取。
'''

# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json

auth_refresh_url = ''
sckey = 'SCU125912Tea3c67d52932a8ee8fbacc30c5a06a675facd045a1968'

ftqq_url = "https://sc.ftqq.com/%s.send"%(sckey)
#两个签到
url1 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2'
url2 = 'https://v.qq.com/x/bu/mobile_checkin'

url3 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=1'#观看60分钟
url4 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=7'#下载
url5 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=6'#赠送
url6 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=3'#弹幕

login_headers = {
    'Referer': 'https://v.qq.com',
    'Cookie': 'tvfe_boss_uuid=********; pgv_pvid=********; video_guid=***********; video_platform=2; pgv_info=ssid=***********; pgv_pvi=*************; pgv_si=*************; _qpsvr_localtk=***************; ptisp=; ptui_loginuin=************; RK=*************; ptcz=***************; main_login=qq; vqq_access_token=****************; vqq_appid=101483052; vqq_openid=********************; vqq_vuserid=*********************; vqq_vusession=dzsfo; vqq_refresh_token=*****************; uid=**************;'
}

login = requests.get(auth_refresh_url, headers=login_headers)
cookie = requests.utils.dict_from_cookiejar(login.cookies)

if not cookie:
    print "auth_refresh error"
    payload = {'text': '腾讯视频V力值签到通知', 'desp': '获取Cookie失败，Cookie失效'}
    requests.post(ftqq_url, params=payload)

sign_headers = {
    'Cookie': 'tvfe_boss_uuid=***********; pgv_pvid=***************; video_guid=***************; video_platform=2; pgv_info=ssid=****************; pgv_pvi=****************; pgv_si=***************; _qpsvr_localtk=*************; ptisp=; ptui_loginuin=***************; RK=****************; ptcz=*********************; main_login=qq; vqq_access_token=************; vqq_appid=101483052; vqq_openid=*************; vqq_vuserid=*************; vqq_vusession=' + cookie['vqq_vusession'] + ';'
    'Referer': 'https://m.v.qq.com'
}
def respondHandle( str ):
    if '-777903' in str:
        return "已获取过V力值"
    elif '-777902' in str:
        return "任务未完成"
    elif 'OK' in str:
        return "成功，获得V力值：" + str[42:-3]
    else:
        return "执行出错"
    

def start():
  sign1 = requests.get(url1,headers=sign_headers).text
  if 'Account Verify Error' in sign1:
    print 'Sign1 error,Cookie Invalid'
    status = "链接1 失败，Cookie失效"
  else:
    print 'Sign1 Success'
    status = "链接1 成功，获得V力值：" + sign1[42:-14]

  sign2 = requests.get(url2,headers=sign_headers).text
  if 'Unauthorized' in sign2:
    print 'Sign2 error,Cookie Invalid'
    status = status + "\n\n 链接2 失败，Cookie失效"
  else:
    print 'Sign2 Success'
    status = status + "\n\n 链接2 成功"
  
  sign3 = requests.get(url3,headers=sign_headers).text
  sign3 = respondHandle(sign3)
  status = status + "\n\n 看60分钟，" + sign3

  sign4 = requests.get(url4,headers=sign_headers).text
  sign4 = respondHandle(sign4)
  status = status + "\n\n 下载视频，" + sign4
  
  sign5 = requests.get(url5,headers=sign_headers).text
  sign5 = respondHandle(sign5)
  status = status + "\n\n 赠送影片，" + sign5
    
  sign6 = requests.get(url6,headers=sign_headers).text
  sign6 = respondHandle(sign6)
  status = status + "\n\n 发送弹幕，" + sign6
  
  payload = {'text': '腾讯视频V力值签到通知', 'desp': status}
  requests.post(ftqq_url, params=payload)

def main_handler(event, context):
  return start()
if __name__ == '__main__':
  start()
