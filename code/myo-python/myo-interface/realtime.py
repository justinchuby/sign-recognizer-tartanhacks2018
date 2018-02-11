# Copyright (c) 2015  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import division, print_function

import myo as libmyo; libmyo.init("../../sdk/myo.framework")
import time
import csv, sys, math, os
import numpy as np
from svmutil import *


class Listener(libmyo.DeviceListener):
    """
    Listener implementation. Return False from any function to
    stop the Hub.
    """

    interval = 0.02  # Output only 0.02 seconds

    def __init__(self):
        super(Listener, self).__init__()
        self.orientation = None
        self.gyroscope = None
        self.acceleration = None
        self.rssi = None
        self.pose = libmyo.Pose.rest
        self.data = []
        self.accl = []
        self.data_locked = False
        self.emg_enabled = False
        self.locked = False
        self.last_time = 0
        self.finalresult = None


    def get_vector(self):

        def make2dList(rows, cols):
            a=[]
            for row in range(rows): a += [[0]*cols]
            return a

        def interpolate(L, length):
            xp = np.linspace(0, len(L), num=len(L))
            x = np.linspace(0, len(L), num=length)
            fp = L
            return np.interp(x, xp, fp)

        #mutex is now locked
        self.data = np.array(self.data) 
        self.data = self.data.transpose()
        #print("transposed data: ", self.data) 
        result0 = make2dList(len(self.data), len(self.data[0]))

        for i in range(len(result0)):
            result0[i] = interpolate(self.data[i], 100)

        result = np.array(result0, dtype='float64')
        
        self.data = []

        #unlock data
        self.data_locked = False
       
        return result 

    def get_gesture(self, vector, modelpath):
       
        def read_range(rangepath):
            par = []
            f = open(rangepath, 'r')
            while 1:
                s = f.readline()
                if not s: break
                tmp = s.split(" ")
                if len(tmp) == 3:
                    if tmp[0] != '-1':
                        par.append([float(tmp[1]), float(tmp[2][:-1])])
            f.close()
            return par

        def scale(vector, rangepath):
            result = vector
            par = read_range(rangepath)
            lower = -1.0
            upper = 1.0
            for index in range(len(result)):
                val = result[index]
                feat_min = par[index][0]
                feat_max = par[index][1]
                if (feat_min == feat_max):
                    return
                if (val == feat_min):
                    result[index] = lower
                elif(val == feat_max):
                    result[index] = upper
                else:
                    result[index] = lower + (upper-lower) * (val-feat_min)/(feat_max-feat_min)
                    if (result[index] > 1) : result[index] = upper
                    if (result[index] < -1) : result[index] = lower
            return result

        #print(svm_dict)
        vector = list(vector)
        labels = []
        # for model in os.listdir(modelpath):
        #     if (".DS_Store" != model):
        #         #print("model name :", model, "\n")
        #         suffix = model.index('.')
        #         name = model[0:suffix]
        #         rangename = "range/" + name + ".data.range"
        #         trans_vector = scale(vector, rangename)
        #         print(modelpath+"/"+model)
        #         (pred_labels, (ACC, MSE, SCC), pred_values) = svm_predict([-1], [trans_vector], svm_load_model(modelpath+"/"+model))
        #         labels.append((model, pred_labels[0]))
        #         #print("labels are: ", labels, "\n")
        trans_vector = scale(vector,"range/hello.data.range")

        (pred_labels0, (ACC, MSE, SCC), pred_values) = svm_predict([-1], [trans_vector], svm_load_model("model/hello.data.model"))
        (pred_labels1, (ACC, MSE, SCC), pred_values) = svm_predict([-1], [trans_vector], svm_load_model("model/my.data.model"))
        (pred_labels2, (ACC, MSE, SCC), pred_values) = svm_predict([-1], [trans_vector], svm_load_model("model/name.data.model"))
        (pred_labels3, (ACC, MSE, SCC), pred_values) = svm_predict([-1], [trans_vector], svm_load_model("model/tartan.data.model"))
        #(pred_labels4, (ACC, MSE, SCC), pred_values) = svm_predict([-1], [trans_vector], svm_load_model("model/hacks.data.model"))
        (pred_labels4, (ACC, MSE, SCC), pred_values) = svm_predict([-1], [trans_vector], svm_load_model("model/whatsup.data.model"))
        # predict = []
        # for tag in labels:
        #     if tag[1] == 1: 
        #         predict.append[tag[0]]
        # if (len(predict) == 0):
        #     return "Retry"
        # elif (len(predict) > 1):
        #     return "Retry"
        pred_labels = [pred_labels0, pred_labels1, pred_labels2, pred_labels3, pred_labels4]

        if (pred_labels0[0] > 0): self.finalresult = "hello"
        if (pred_labels1[0] > 0): self.finalresult = "my"
        if (pred_labels2[0] > 0): self.finalresult = "name"
        if (pred_labels3[0] > 0): self.finalresult = "tartan"
        if (pred_labels4[0] > 0): self.finalresult = "whatsup"

        print("this is: ", self.finalresult)
        #self.finalresult = predict[0]
        return self.finalresult

    def get_data(self):
        #current time stamp
        # ctime = time.time()
        # if (ctime - self.last_time) < self.interval:
        #     return
        # self.last_time = ctime

        #if all eles in a is greater than val return true
        def comp(a, val):
            for ele in a:
                if (ele < val): return False
            return True 

        if self.acceleration:
            #placeholder for values
            tmp = []
            #print("acceleration: ", self.acceleration[0])
            #print(" ", self.data_locked)
            self.accl.append(self.acceleration[0])

            if (not self.data_locked):
                if (self.accl[-1] < 0.85):
                    #print("start recording.........\n")
                    if self.gyroscope and self.orientation:
                        for val in self.gyroscope:
                            tmp.append(val)

                        #calculate orientationeuler
                        x = self.orientation[0]
                        y = self.orientation[1]
                        z = self.orientation[2]
                        w = self.orientation[3]

                        roll = np.arctan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
                        pitch = np.arcsin(max(-1.0, min(1.0, 2.0 * (w * y - z * x))))
                        yaw = np.arctan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))

                        tmp.extend([roll,pitch,yaw])

                        self.data.append(tmp)
                        
                        #print(len(self.data))
                        #print(self.data)

                if (self.accl[-1] > 0.9):
                    #print("rest mode............\n")
                    #eliminate noise
                    if (not self.data_locked) and (len(self.data) < 50): 
                        self.data = []
                    #if rest pose
                    if (comp(self.accl[-20:], 0.9)):
                        #print("accl:", self.accl[-20:])
                        self.accl = self.accl[:-21]
                        #print("rest pose, truncate data")
                        self.data = self.data[:-21]

                        if (not self.data_locked) and (self.data != []) and (len(self.data) >= 50):
                        
                            #print("running scale...............\n")
                            self.data_locked = True
                            result = self.get_vector()
                            vector = result.flatten()
                            #print("result", vector)
                            label = self.get_gesture(vector, "model")
                            print(label)
                            return label

    def on_connect(self, myo, timestamp, firmware_version):
        myo.vibrate('short')
        myo.vibrate('short')
        myo.request_rssi()
        myo.request_battery_level()

    def on_rssi(self, myo, timestamp, rssi):
        pass

    def on_pose(self, myo, timestamp, pose):
        if pose == libmyo.Pose.double_tap:
            myo.set_stream_emg(libmyo.StreamEmg.enabled)
            self.emg_enabled = True
        elif pose == libmyo.Pose.fingers_spread:
            myo.set_stream_emg(libmyo.StreamEmg.disabled)
            self.emg_enabled = False
            self.emg = None
        self.pose = pose
        self.get_data()

    def on_orientation_data(self, myo, timestamp, orientation):
        self.orientation = orientation
        self.get_data()

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        self.acceleration = acceleration
        self.get_data()

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        self.gyroscope = gyroscope
        self.get_data()

    def on_emg_data(self, myo, timestamp, emg):
        pass

    def on_unlock(self, myo, timestamp):
        self.locked = False
        self.get_data()

    def on_lock(self, myo, timestamp):
        self.locked = True
        self.get_data()

    def on_event(self, kind, event):
        """
        Called before any of the event callbacks.
        """

    def on_event_finished(self, kind, event):
        """
        Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub.
        """

    def on_pair(self, myo, timestamp, firmware_version):
        """
        Called when a Myo armband is paired.
        """

    def on_unpair(self, myo, timestamp):
        """
        Called when a Myo armband is unpaired.
        """

    def on_disconnect(self, myo, timestamp):
        """
        Called when a Myo is disconnected.
        """

    def on_arm_sync(self, myo, timestamp, arm, x_direction, rotation,
                    warmup_state):
        """
        Called when a Myo armband and an arm is synced.
        """

    def on_arm_unsync(self, myo, timestamp):
        """
        Called when a Myo armband and an arm is unsynced.
        """

    def on_battery_level_received(self, myo, timestamp, level):
        """
        Called when the requested battery level received.
        """

    def on_warmup_completed(self, myo, timestamp, warmup_result):
        """
        Called when the warmup completed.
        """

listener = None
def main():
    print("Connecting to Myo ... Use CTRL^C to exit.")
    try:
        hub = libmyo.Hub()
    except MemoryError:
        print("Myo Hub could not be created. Make sure Myo Connect is running.")
        return

    hub.set_locking_policy(libmyo.LockingPolicy.none)
    global listener
    listener = Listener()
    hub.run(1000, listener)

    # Listen to keyboard interrupts and stop the hub in that case.
    try:
        while hub.running:
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nQuitting ...")
    finally:
        print("Shutting down hub...")
        hub.shutdown()


if __name__ == '__main__':
    main()

