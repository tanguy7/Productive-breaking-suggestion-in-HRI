#!/usr/bin/env python3

# imports
import numpy as np
import rospy
import smach
import roslib
import smach_ros
from std_msgs.msg import String
import time
import subprocess
import csv
from qt_robot_interface.srv import *
from qt_gesture_controller.srv import gesture_play
from qt_motors_controller.srv import *
from std_msgs.msg import Float64MultiArray

import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import pickle # Used to save the model
import pandas as pd
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from pathlib import Path
from std_msgs.msg import String
import warnings

warnings.filterwarnings("ignore")

# Initialisation of global variables
group = 1
score1_1 = None
score1_2 = None
score1_3 = None
score2_1 = None
score2_2 = None
score2_3 = None
score3_1 = None
score3_2 = None
score3_3 = None
time1_1 = None
time1_2 = None
time1_3 = None
time2_1 = None
time2_2 = None
time2_3 = None
time3_1 = None
time3_2 = None
time3_3 = None

class Waiting(smach.State):
    """Waits until the user is detected on the camera"""
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'],
                             input_keys=['arms'])

    def execute(self, userdata):
        rospy.loginfo('---Waiting---')
        rospy.sleep(5.)
        while(userdata.arms == 'Not here'):
            rospy.sleep(2.)
            pass
        return 'proceed'

class Form1(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed1', 'proceed2'])
    def execute(self, userdata):
        global group
        msg = 'Tell me how you feel by filling the form displayed on the screen. Then click on submit !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)

        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/stai1.py'])

        msg = 'Thanks!'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)

        if group == '1':
            return 'proceed1'
        else:
            return 'proceed2'


class Form2(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'])

    def execute(self, userdata):
        global group

        msg = 'Please fill the form displayed on the screen.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)

        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/stai2.py'])

        msg = 'Thank you !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        return 'proceed'


class Form3(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed1', 'proceed2'])

    def execute(self, userdata):
        global group
        msg = 'Like before, I need you to tell me how you feel at this moment.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)

        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/stai3.py'])

        msg = 'Thanks a lot!'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        if group == '1':
            return 'proceed1'
        else:
            return 'proceed2'


class Form4(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'])

    def execute(self, userdata):
        global group
        msg = 'How do you feel ? Answer the form a last time please.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)

        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/stai4.py'])

        msg = 'Thank you !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        return 'proceed'


class Memory1(smach.State):
    """First time launching the sequence of memory games"""
    def __init__(self):
            smach.State.__init__(self,
                                 outcomes=['proceed'])

    def execute(self, userdata):
        global score1_1
        global score1_2
        global score1_3
        global time1_1
        global time1_2
        global time1_3
        msg = 'We are going to play some memory games.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        msg = 'I will make the first game pop up on the screen. You have one attempt for each game. Try do do your best!'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/number_game.py'])
        time1_1 = time.time()-start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score1_1 = int(score)
        if score1_1 >  7:
            msg = 'Good job ! ' + score + 'numbers is a good score ! Now play the second game.'
        elif score1_1 < 6:
            msg = 'I think you can do better ! You will retry later! Now play the second game.'
        else :
            msg = 'Good job ! Now play the second game'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/word_game.py'])
        time1_2 = time.time()-start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score1_2 = int(score)
        msg = 'Now we finish with the last memory game, good luck!'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/visual_game.py'])
        time1_3 = time.time() - start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score1_3 = int(score)
        msg = 'Well done !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        return 'proceed'


class Memory2(smach.State):
    """Second time launching the sequence of memory games"""
    def __init__(self):
            smach.State.__init__(self,
                                 outcomes=['proceed'])

    def execute(self, userdata):
        global score1_1
        global score1_2
        global score1_3
        global score2_1
        global score2_2
        global score2_3
        global time2_1
        global time2_2
        global time2_3
        msg = 'You are going to play the memory games a second time, try to improve your results!'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/number_game.py'])
        time2_1 = time.time()-start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score2_1 = int(score)
        if score2_1 > score1_1 :
            diff = score2_1 - score1_1
            convert = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
            msg = 'Wow, you did better than the first time! Your remembered ' + convert[diff] + ' more numbers!'
        else :
            msg = 'Good job ! You can play the second game'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/word_game.py'])
        time2_2 = time.time()-start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score2_2 = int(score)
        if score2_2 > score1_2 :
            diff = score2_2 - score1_2
            convert = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
            if convert[diff] == 'one':
                end = ' word'
            else:
                end = ' words'
            msg = 'Wow! You improved your result by ' + convert[diff] + end +'! Now, play the last game!'
        else :
            msg = 'Now you play the last game'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/visual_game.py'])
        time2_3 = time.time()-start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score2_3 = int(score)
        return 'proceed'

class Memory3(smach.State):
    """Third time launching the sequence of memory games"""
    def __init__(self):
            smach.State.__init__(self,
                                 outcomes=['proceed'])

    def execute(self, userdata):
        global score1_1
        global score1_2
        global score1_3
        global score2_1
        global score2_2
        global score2_3
        global score3_1
        global score3_2 
        global score3_3
        global time3_1
        global time3_2
        global time3_3
        msg = 'We are now playing the memory games for one last time. Try to set new highscores !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/number_game.py'])
        time3_1 = time.time()-start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score3_1 = int(score)
        if (score3_1 > score2_1) and (score3_1 > score1_1):
            msg = 'You set a new highscore! Here is the second game!'
        else : 
            msg = 'Well done! Here is the second game'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/word_game.py'])
        time3_2 = time.time()-start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score3_2 = int(score)
        if (score3_2 > score2_2) and (score3_2 > score1_2):
            msg = 'It is your best result, good job! You can play the last game !'
        else : 
            msg = 'You can play the last game !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        start = time.time()
        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/visual_game.py'])
        time3_3 = time.time()-start
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    score = str(char)
                    score3_3 = int(score)
        if (score3_3 > score2_3) and (score3_3 > score1_3):
            msg = 'Nice ! You did better than the other times!'
        return 'proceed'

class Free_time(smach.State):
    """Launches the free time break"""
    def __init__(self):
            smach.State.__init__(self,
                                 outcomes=['proceed1','proceed2'])

    def execute(self, userdata):
        global group
        msg = 'You have a few minutes of free time now. Do whatever you want! Enjoy your break, I will call you back when we continue the activities.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        rospy.sleep(100.)
        msg = 'We continue in one minute !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        rospy.sleep(60.)
        msg = 'I hope you were not bored. Lets continue the activities'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        if group == '1':
            return 'proceed1'
        else:
            return 'proceed2'

class Welcome(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'])

    def execute(self, userdata):
        rospy.loginfo('---Executing state Welcome---')
        global group
        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('QT/happy', 0)

        emotionShow = rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
        rospy.wait_for_service('/qt_robot/emotion/show')
        emotionShow('QT/happy')

        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay("Hello, my name is QT ! Thanks for coming at the lab to see me. Lets begin !")

        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay("I need you to use the keyboard to enter your name and choose your group.")

        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('pointing', 2)

        subprocess.call(['python3', '/home/tanguy/catkin_ws/src/state_machine/scripts/login.py'])
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'r') as file:
            lines = file.readlines()
            last_line = str(lines[-1:])
            for char in last_line:
                if char.isdigit():
                    group = str(char)
            rospy.loginfo(group)
        return 'proceed'

class Head_left(smach.State):
    """Head to the left stretch."""
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'],
                             input_keys=['head'])

    def execute(self, userdata):
        rospy.loginfo('Executing head left stretch')

        emotionShow = rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
        rospy.wait_for_service('/qt_robot/emotion/show')
        emotionShow('QT/neutral')

        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay("I stood still for a very long time, I really need some stretching !")

        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('stretch', 1)
 
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay("Lets do a stretch session together, it will be fun !")

        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay("We start with the head. I will show you how to do each stretch. Your stretch should last at least five seconds and I will count to five when you do it.")
        # added
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay("You should start stretching when I show you how to do it. But you need to maintain the position for more time than me, until I finish counting.")
        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('head_left', 1.5)

        seconds = 0
        start_time = time.time()

        # Stretch stop either when the subject has done it for five seconds or after 25 seconds
        while (seconds < 5) and (time.time()-start_time < 25) :
            if(userdata.head != 'Head_left'):
                pass
            else :
                seconds = seconds + 1
                numbers = ['one', 'two', 'three', 'four', 'five']
                msg = numbers[seconds-1]
                speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
                rospy.wait_for_service('/qt_robot/speech/say')
                speechSay(msg)
                rospy.sleep(0.5)
        emotionShow = rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
        rospy.wait_for_service('/qt_robot/emotion/show')
        emotionShow('QT/happy')
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay("Great ! The next stretch is moving the head up.")
        return 'proceed'

class Head_up(smach.State):
    """Head up stretch."""

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'],
                             input_keys=['head'])

    def execute(self, userdata):
        rospy.loginfo('Executing head up stretch')
        msg = 'Let me show you. Keep the head up until I finish counting.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('head_up', 1.5)
 
        seconds = 0
        start_time = time.time()

        while (seconds < 5) and (time.time()-start_time < 25) :
            if(userdata.head != 'Head_up'):
                pass
            else:
                seconds = seconds + 1
                numbers = ['one', 'two', 'three', 'four', 'five']
                msg = numbers[seconds-1]
                speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
                rospy.wait_for_service('/qt_robot/speech/say')
                speechSay(msg)
                rospy.sleep(0.5)
        msg = 'Nice, lets move on. Next stretch is keeping the head down.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        return 'proceed'

class Head_down(smach.State):
    """Head down stretch."""

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'],
                             input_keys =['head'])

    def execute(self, userdata):
        rospy.loginfo('Executing head down stretch')
        msg = 'I show you the position'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('head_down', 1.5)

        seconds = 0
        start_time = time.time()

        while (seconds < 5) and (time.time()-start_time < 25) :
            if(userdata.head != 'Head_down'):
                pass
            else:
                seconds = seconds + 1
                numbers = ['one', 'two', 'three', 'four', 'five']
                msg = numbers[seconds-1]
                speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
                rospy.wait_for_service('/qt_robot/speech/say')
                speechSay(msg)
                rospy.sleep(0.5)
        msg = 'Perfect! We continue. Next, we move our head to the right!'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        return 'proceed'

class Head_right(smach.State):
    """Head to the right stretch."""

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'],
                             input_keys =['head'])

    def execute(self, userdata):
        rospy.loginfo('Executing head right stretch')
        msg = 'Just like that.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)

        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('head_right', 1.5)

        seconds = 0
        start_time = time.time()
        while (seconds < 5) and (time.time()-start_time < 25) :
            if(userdata.head != 'Head_right'):
                pass
            else:
                seconds = seconds + 1 
                numbers = ['one', 'two', 'three', 'four', 'five']
                msg = numbers[seconds-1]
                speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
                rospy.wait_for_service('/qt_robot/speech/say')
                speechSay(msg)
                rospy.sleep(0.5)
        msg = 'Nice, lets move on to the next stretch.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        return 'proceed'

class Wide_arms(smach.State):
    """Wide arms stretch."""

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'],
                             input_keys =['arms'])

    def execute(self, userdata):
        rospy.loginfo('Executing wide arms stretch')
        msg = 'You can widen your arms with me. Do not forget to maintain the stretch until I finish counting.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('wide_arms', 1.5)
        seconds = 0
        start_time = time.time()

        while (seconds < 5) and (time.time()-start_time < 25) :
            if(userdata.arms != 'Wide_arms'):
                pass
            else : 
                seconds = seconds + 1
                numbers = ['one', 'two', 'three', 'four', 'five']
                msg = numbers[seconds-1]
                speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
                rospy.wait_for_service('/qt_robot/speech/say')
                speechSay(msg)
                rospy.sleep(0.5)
        emotionShow = rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
        rospy.wait_for_service('/qt_robot/emotion/show')
        emotionShow('QT/happy')
        msg = 'Nice, lets move on to the last stretch.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        return 'proceed'

class Arms_up(smach.State):
    """Arms up stretch"""

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'],
                             input_keys =['arms'])

    def execute(self, userdata):
        rospy.loginfo('Executing arms up stretch')
        msg = 'Raise your arms with me !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        rospy.wait_for_service('/qt_robot/gesture/play')
        gesturePlay('hands_up', 1.5)
        seconds = 0
        start_time = time.time()

        while (seconds < 5) and (time.time()-start_time < 25) :
            if(userdata.arms != 'Arms_up'):
                pass
            else :
                seconds = seconds + 1
                numbers = ['one', 'two', 'three', 'four', 'five']
                msg = numbers[seconds-1]
                speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
                rospy.wait_for_service('/qt_robot/speech/say')
                speechSay(msg)
                rospy.sleep(0.5)
        msg = 'Good job!'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        msg = 'Well done, we finished the stretch session. I feel way better!'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        emotionShow = rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
        rospy.wait_for_service('/qt_robot/emotion/show')
        emotionShow('QT/happy')
        return 'proceed'

class Breathe(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed1', 'proceed2'])

    def execute(self, userdata):
        global group
        rospy.loginfo('Executing breathing state')
        msg = 'We are now going to do some deep breathing !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        msg = 'Sit straight in your chair.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        msg = 'We are going to start. When I say in, inhale through the nose. When I say out, exhale through the mouth'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        rospy.sleep(1.)
        for i in range(6):
            msg = 'In'
            speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
            rospy.wait_for_service('/qt_robot/speech/say')
            speechSay(msg)
            rospy.sleep(4.)
            msg = 'Out'
            speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
            rospy.wait_for_service('/qt_robot/speech/say')
            speechSay(msg)
            rospy.sleep(4.)
        msg = 'Great, you did good !'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)
        if group == '1':
            return 'proceed1'
        else:
            return 'proceed2'


class Goodbye(smach.State):
    """Ending the interaction."""

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['proceed'])
    
    def execute(self, userdata):
        global time1_1
        global time1_2
        global time1_3
        global time2_1
        global time2_2
        global time2_3
        global time3_1
        global time3_2
        global time3_3
        rospy.loginfo('Executing state Goodbye')
        msg = 'Goodbye my friend, thank you for playing with me.'
        speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        rospy.wait_for_service('/qt_robot/speech/say')
        speechSay(msg)

        # writing all the times in the csv file
        results = ['times',time1_1,time1_2,time1_3,time2_1,time2_2, time2_3, time3_1, time3_2, time3_3]
        with open('/home/tanguy/catkin_ws/src/state_machine/scripts/logs.csv', 'a', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(results)


        return 'proceed'


class Manager():
    def __init__(self):
        # Models for detection of movements 
        self.mp_drawing = mp.solutions.drawing_utils # Drawing helpers
        self.mp_holistic = mp.solutions.holistic # Mediapipe Solutions

        # Reloading our model
        HERE = Path(__file__).parent

        with open(HERE /'neck_stretches.pkl', 'rb') as g: #reading
            self.neck_model = pickle.load(g)
        with open(HERE / 'arm_stretches.pkl', 'rb') as f: #reading
            self.arm_model = pickle.load(f)

        self.bridge = CvBridge()

        # initialize ROS node
        rospy.init_node('stretch_manager', anonymous=True)

        rospy.Subscriber('/camera/color/image_raw', Image, self.image_callback)

        # create a SMACH state machine
        self.sm = smach.StateMachine(outcomes=['end'])

        self.sm.userdata.head = ''
        self.sm.userdata.arms = ''

        rospy.loginfo("Starting Manager")

        # open the container
        with self.sm:
            # Add states to the container
            # Waiting for the detection of one person
            smach.StateMachine.add('WAITING', Waiting(),
                                    transitions={'proceed':'WELCOME'})
            # State welcoming the user and making him choose between the two programs
            smach.StateMachine.add('WELCOME', Welcome(),
                                    transitions={'proceed':'MEMORY1'})
            smach.StateMachine.add('FORM1', Form1(),
                                    transitions={'proceed1':'HEAD_LEFT', 'proceed2':'FREE_TIME'})
            smach.StateMachine.add('FORM2', Form2(),
                                    transitions={'proceed':'MEMORY2'})
            smach.StateMachine.add('FORM3', Form3(),
                                    transitions={'proceed1':'FREE_TIME', 'proceed2':'HEAD_LEFT'})
            smach.StateMachine.add('FORM4', Form4(),
                                    transitions={'proceed':'MEMORY3'})
            smach.StateMachine.add('MEMORY1', Memory1(),
                                    transitions={'proceed' : 'FORM1'})   
            smach.StateMachine.add('MEMORY2', Memory2(),
                                    transitions={'proceed' : 'FORM3'})   
            smach.StateMachine.add('MEMORY3', Memory3(),
                                    transitions={'proceed' : 'GOODBYE'})   
            smach.StateMachine.add('FREE_TIME', Free_time(),
                                    transitions={'proceed1':'FORM4', 'proceed2':'FORM2'})
            smach.StateMachine.add('HEAD_LEFT', Head_left(),
                                    transitions={'proceed':'HEAD_UP'})
            smach.StateMachine.add('HEAD_UP', Head_up(),
                                    transitions={'proceed':'HEAD_DOWN'})
            smach.StateMachine.add('HEAD_DOWN', Head_down(),
                                    transitions={'proceed':'HEAD_RIGHT'})
            smach.StateMachine.add('HEAD_RIGHT', Head_right(),
                                    transitions={'proceed':'WIDE_ARMS'})
            smach.StateMachine.add('WIDE_ARMS', Wide_arms(),
                                    transitions={'proceed':'ARMS_UP'})
            smach.StateMachine.add('ARMS_UP', Arms_up(),
                                    transitions={'proceed':'BREATHE'})
            # TO DO : ADD BREATHING STATE
            smach.StateMachine.add('BREATHE', Breathe(),
                                    transitions={'proceed1':'FORM2', 'proceed2':'FORM4'})
            smach.StateMachine.add('GOODBYE', Goodbye(),
                                    transitions={'proceed':'end'})  

        self.sm.set_initial_state(['WAITING'])

        # execute SMACH plan
        outcome = self.sm.execute()
        rospy.loginfo("OUTCOME: " + outcome)
        rospy.spin()




    def image_callback(self, data):
        global my_image
        rate = rospy.Rate(2)
        try:
            my_image = self.bridge.imgmsg_to_cv2(data,"bgr8")

            with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False   
                results = holistic.process(image)
                
                # Recolor image back to BGR for rendering
                image.flags.writeable = True   
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

                # Export coordinates
                try:

                    face = results.face_landmarks.landmark
                    face_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())
                    face_X = pd.DataFrame([face_row])
                    face_stretch_class = self.neck_model.predict(face_X)[0]
                    
                except:
                    face_stretch_class = 'Not here'
                    pass 

                msg = face_stretch_class
                self.sm.userdata.head = msg
                rate.sleep()

            with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                
                # Recolor Feed
                image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False        
                
                # Make Detections
                results = holistic.process(image)
                
                # Recolor image back to BGR for rendering
                image.flags.writeable = True   
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    # Extract Pose landmarks
                    pose = results.pose_landmarks.landmark
                    pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())

                    # Make Detections
                    pose_X = pd.DataFrame([pose_row])
                    arm_stretch_class = self.arm_model.predict(pose_X)[0]

                except:
                    arm_stretch_class = 'Not here'
                    pass
                
                msg = arm_stretch_class
                self.sm.userdata.arms = msg
 

        except CvBridgeError as e:
            print(e)
        else:
            pass


if __name__ == "__main__":
    try:
        myManager = Manager()
    except rospy.ROSInterruptException:
        pass
