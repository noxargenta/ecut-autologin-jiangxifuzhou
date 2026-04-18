import requests
import time
import os

# ================= 配置区 =================
# 建议通过环境变量获取，保护隐私
USERNAME = os.getenv("SCHOOL_USER", "你的账号@fzcmcc")
# 运营商类型后缀示例 (加在学号后)中国移动@fzcmcc  或@cmcc
#  中国电信@telecom 或 @dx
#  中国联通@unicom @lt
#  校园网自办@xyw 或 (留空)
#  可以自行开F12抓包查看后缀是什么，目前我知道的是ECUT移动的是fzcmcc。
PASSWORD = os.getenv("SCHOOL_PWD", "你的密码")
# 认证服务器地址 (ECUT 默认通常为 172.30.255.105)
AUTH_SERVER = "172.30.255.105"
# ==========================================

class EcutUpdater:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': f'http://{AUTH_SERVER}/'
        })

    def logout(self):
        """注销当前连接"""
        url = f"http://{AUTH_SERVER}:801/eportal/"
        params = {'c': 'ACSetting', 'a': 'Logout'}
        try:
            self.session.get(url, params=params, timeout=5)
            print("[Info] 登出请求已发送")
            time.sleep(1.5) # 等待服务器释放连接
        except Exception as e:
            print(f"[Error] 登出异常: {e}")

    def login(self):
        """执行登录"""
        url = f"http://{AUTH_SERVER}:801/eportal/"
        # 获取当前时间戳作为回调
        callback_id = f"dr{int(time.time() * 1000)}"
        
        params = {
            'c': 'Portal',
            'a': 'login',
            'callback': callback_id,
            'login_method': '1',
            'user_account': USERNAME,
            'user_password': PASSWORD,
            'wlan_user_ip': '', # 留空通常由服务器自动识别
            'wlan_user_mac': '000000000000',
            'jsVersion': '3.0'
        }
        
        try:
            res = self.session.get(url, params=params, timeout=5)
            if '"result":"1"' in res.text:
                print(f"[Success] 账号 {USERNAME} 登录成功！")
            else:
                print(f"[Failed] 登录失败，服务器返回: {res.text[:50]}")
        except Exception as e:
            print(f"[Error] 连接认证服务器失败: {e}")

if __name__ == "__main__":
    worker = EcutUpdater()
    worker.logout()
    worker.login()