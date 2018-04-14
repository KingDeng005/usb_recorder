#!/usr/bin/env python
# Created by Fuheng Deng on 6/23/2017

import subprocess
from datetime import datetime, timedelta
import traceback
import os
import time
import rospy

class Recorder():

    def __init__(self):
        self.record_proc = None
        self.process_proc = None
        self.current_folder = ''

    @staticmethod
    def _check_video():
        try:
            devs = os.listdir('/dev')
            return len([dev for dev in devs if dev.startswith('video')]) > 0
        except OSError:
            rospy.logerror('cannot open up dev, msg: {}'.format(traceback.format_exc()))
            return 0
    
    @staticmethod
    def _ckeck_audio():
        # TO-DO
        return false

    def start_record(self, dir):
        # create folder if not done so
        self.current_folder = dir
        if not os.path.exists(self.current_folder):
            os.makedirs(self.current_folder)

        # check input
        if not self._check_video():
            print('video device not found')
            return

        if not self._check_audio():
            print('audio device not found')
            return

        # record only when both video and audio exist
        cmd = ['roslaunch', 'recorder', 'record_launch.launch']
        cmd.append('usb_cam:=true')
        cmd.append('video:=true')
        cmd.append('audio:=true')
        cmd.append('dir:=' + self.current_folder)
        self.record_proc = subprocess.Popen(cmd)

    def stop_record(self, save=True, clear=True):
        if self.record_proc != None and self.record_proc.poll() == None:
            self.record_proc.terminate()
            self.record_proc.wait()
            if save:
                # start processing the video
                cmd = []
                cmd.append('ffmpeg')
                cmd.append('-i')
                cmd.append(self.current_folder + '/output.avi')
                cmd.append('-i')
                cmd.append(self.current_folder + '/output.mp3')
                cmd.append('-c')
                cmd.append('copy')
                cmd.append(self.current_folder + '/output.mp4')
                self.process_proc = subprocess.check_call(cmd)
            if clear:
                # remove the pre-files
                cmd = ['rm', '-rf']
                cmd.append(self.current_folder + '/output.avi')
                cmd.append(self.current_folder + '/output.mp3')
                self.process_proc = subprocess.check_call(cmd)

if __name__ == "__main__":
    recorder = Recorder()
    recorder.start_record(dir='/home/fuheng/usb_cam_recorder/') 
    recorder.stop_record()
