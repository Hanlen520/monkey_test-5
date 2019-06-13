from src.readConfig import Readconfig
from src.global_parameter import project_path, monkey_log_path
import os, time, subprocess, re


class Runmonkey():
    def __init__(self):
        self.read_config = Readconfig()
        self.apk_path = project_path + "\\apk\\" + self.read_config.get_config_values("appinfo","apk_name")
        self.log_path = monkey_log_path

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

    def install_apk(self):
        print("Ready to start installing apk")
        cmd = "adb -s %s install -r %s"%(self.deviceid, self.apk_path)
        os.popen(cmd)

    def kill_test_app(self):
        cmd = "adb -s %s shell am force-stop %s"%(self.deviceid, self.package_name)
        print(cmd)
        os.popen(cmd)

    def full_monkey(self):
        device_ids = self.get_device_id()
        for device_id in device_ids:
            self.install_apk()
            monkey_cmd = "adb -s %s shell monkey -p %s --throttle 100 --pct-touch 70 --pct-motion 5 --pct-nav 0 " \
                     "--pct-trackball 0 --pct-majornav 5 --ignore-crashes --ignore-timeouts --pct-appswitch " \
                     "10 --pct-syskeys 5 -v-v-v 100 >%s"%(self.deviceid, self.package_name, self.log_path)
        print(monkey_cmd)
        self.kill_test_app()




if __name__ == '__main__':
    runmonkey = Runmonkey()
    print(runmonkey.get_package_name())
    runmonkey.get_device_id()