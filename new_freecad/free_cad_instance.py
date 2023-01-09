import subprocess
import sys
import threading
import time
import traceback
from base_define import instance_status
import os


class free_cad_instance:

    def __init__(self, port, wss):
        self.__port = port
        self.__wss = wss
        self.__progress = None
        self.__status = instance_status.PENGING
        self._fp = None
        self.__subProcess = None

    def start_instance(self, cmd, work_folder, log_file, call_back):
        if (log_file.endswith(".txt")):
            self._fp = open(log_file, 'a+', encoding='utf-8')

        command = cmd + self.get_instance_parm()
        self.__progress = self.__start_instance(cmd, work_folder)
        thread1 = threading.Thread(target=self.progress_listening, args=(self.__progress, call_back))
        self.__status = instance_status.RUNING

    def progress_listening(self, progress, call_back):
        while (progress.poll() is None):
            time.sleep(10)
        self.__status = instance_status.CLOSED
        call_back(self.__wss)

    def get_instance_parm(self):
        return " -port " + self.__port

    def __start_instance(self, cmd, workFolder):
        outPrint = sys.stdout
        if (self._fp != None):
            outPrint = self._fp
        p = subprocess.Popen(cmd, shell=True, cwd=workFolder, close_fds=True, stdout=outPrint)
        self.__subProcess = p
        print("self.__subProcess.pid:")
        print(self.__subProcess.pid)
        return p

    def get_status(self):
        return self.__status

    def get_wss(self):
        return self.__wss

    def close_instance(self):
        print("close_instance")
        if (self.__subProcess):
            try:
                os.system('taskkill /t /f /pid {}'.format(self.__subProcess.pid))
            except Exception as e:
                print(traceback.format_exc())
            self.__subProcess = None
            self.__status = instance_status.PENGING
            return 1
        return 0
