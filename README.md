# Productive-breaking-suggestion-in-HRI

In this project we test the effect of two different types of break happening during a HRI on Short-Term Memory (STM). To have a better understanding, please first read [This report](./Semester_project_tanguy.pdf)

We designed three games for testing STM : 'number_game.py', 'word_game.py', 'visual_game.py'
We use 4 forms to measure anxiety : 'stai1.py', 'stai2.py', 'stai3.py', 'stai4.py'

We also trained a model to detect some stretching movements in 'Pose_recognition_training_notebook.ipynb'. This program uses mediapipe to detect body keypoints, and we trained a classifier to detect each stretch based on recorded coordinates of the stretches ('arm_stretches_coords.csv' and 'neck_stretches_coords.csv'. The models we keep for the detection are available : 'neck_stretches.pkl' and 'arm_stretches.pkl'.

'manager.launch' is used to launch 'interaction.py' which is basically a state machine going through each step of the experiment, and where the HRI is coded.
