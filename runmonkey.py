from src.readConfig import Readconfig
from src.global_parameter import project_path, monkey_log_path
import os, subprocess, re,time,threading


class Runmonkey():
    def __init__(self):
        self.read_config = Readconfig()
        self.apk_path = project_path + "\\apk\\" + self.read_config.get_config_values("appinfo","apk_name")
        self.log_path = monkey_log_path
        self.package_name = self.get_package_name()
        self.exx_count = self.read_config.get_config_values("baseinfo","exe_count")

    def get_aapt(self):
        if "ANDROID_HOME" in os.environ:
            root_dir = os.path.join(os.environ["ANDROID_HOME"], "build-tools")
            for path, subdir, files in os.walk(root_dir):
                if "aapt.exe" in files:
                    return os.path.join(path, "aapt.exe")

    def get_app_base_info(self):
        cmd = self.get_aapt() + ' dump badging ' + self.apk_path
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(output.decode())
        match_1 = re.compile("launchable-activity: name='(\S+)'  label=").search(output.decode())
        package_name = match.group(1)
        version_code = match.group(2)
        version_name = match.group(3)
        launchable_activity_name = match_1.group(1)
        return (package_name, version_code, version_name, launchable_activity_name)

    def get_package_name(self):
        t = self.get_app_base_info()
        return t[0]

    def get_device_id(self):
        try:
            cmd = 'adb devices'
            l = os.popen(cmd).readlines()
            device_id = []
            for value in l[1:len(l) - 1]:
                device_id.append(value.split('\t')[0])
            return device_id
        except:
            print("请连接手机")

    def install_apk(self,deviceid):
        print("开始安装APP")
        cmd = "adb -s %s install -r %s"%(deviceid, self.apk_path)
        os.popen(cmd)
        print("APP安装结束")

    def kill_test_app(self,deviceid):
        print("开始杀掉APP进程")
        cmd = "adb -s %s shell am force-stop %s"%(deviceid, self.package_name)
        os.popen(cmd)
        print("APP进程杀掉完成")

    def monkey_run(self, deviceid):
        print("开始运行monkey测试")
        current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        monky_log = self.log_path + current_time + deviceid + ".txt"
        print(monky_log)
        throttle = self.read_config.get_config_values("monkeyinfo","throttle")
        touch = self.read_config.get_config_values("monkeyinfo","touch")
        motion = self.read_config.get_config_values("monkeyinfo","motion")
        nav = self.read_config.get_config_values("monkeyinfo","nav")
        trackball = self.read_config.get_config_values("monkeyinfo","trackball")
        majornav = self.read_config.get_config_values("monkeyinfo","majornav")
        appswitch = self.read_config.get_config_values("monkeyinfo","appswitch")
        syskeys = self.read_config.get_config_values("monkeyinfo","syskeys")
        log = self.read_config.get_config_values("monkeyinfo","log")
        click = self.read_config.get_config_values("monkeyinfo","click")
        monkey_cmd = "adb -s %s shell monkey -p %s --throttle %s --pct-touch %s --pct-motion %s --pct-nav %s " \
                     "--pct-trackball %s --pct-majornav %s --ignore-crashes --ignore-timeouts --ignore-security-exceptions " \
                     "--pct-appswitch " \
                     "%s --pct-syskeys %s %s %s >%s 2>&1 1" % (deviceid, self.package_name,throttle,touch,motion,nav,trackball,majornav,appswitch,syskeys,log,click, monky_log)
        os.popen(monkey_cmd)
        self.kill_test_app(deviceid)
        print("monkey测试运行完成")

    def amount_monkey_run(self,device_id):
        exe_count = int(self.read_config.get_config_values("baseinfo", "exe_count")) - 1
        while (exe_count):
            self.monkey_run(device_id)
            exe_count -= 1


    def full_monkey(self):
        device_ids = self.get_device_id()
        threads = []
        for device_id in device_ids:
            thread_n = threading.Thread(target=self.amount_monkey_run, args=(device_id))
            threads.append(thread_n)

        for thread in threads:
            thread.daemon = True  # 设置守护线程。主线程将在所有非守护线程退出之后才退出。
            thread.start()


if __name__ == '__main__':
    runmonkey = Runmonkey()
    runmonkey.full_monkey()