# Sparse Coding Semantic Hyperlapse

[![Version](https://img.shields.io/badge/version-1.0-brightgreen.svg)](https://www.verlab.dcc.ufmg.br/semantic-hyperlapse)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)

# Project #

This project contains the code and data used to generate the results reported in the paper [A Weighted Sparse Sampling and Smoothing Frame Transition Approach for Semantic Fast-Forward First-Person Videos](https://www.verlab.dcc.ufmg.br/semantic-hyperlapse/papers/) on the **IEEE Conference on Computer Vision and Pattern Recognition (CVPR) 2018**. It implements a Semantic Fast-forward method for First-Person Videos with a proper stabilization method based on a adaptive frame selection via Minimum Sparse Reconstruction problem and Smoothing Frame Transition.

For more information and visual results, please access the [project page](https://www.verlab.dcc.ufmg.br/semantic-hyperlapse).

## Contact ##

### Authors ###

* Michel Melo da Silva - PhD student - UFMG - michelms@dcc.ufmg.com
* Washington Luis de Souza Ramos - PhD student - UFMG - washington.ramos@outlook.com
* João Pedro Klock Ferreira - Undergraduate Student - UFMG - jpklock@ufmg.br
* Felipe Cadar Chamone - Undergraduate Student - UFMG - cadar@dcc.ufmg.br
* Mario Fernando Montenegro Campos - Advisor - UFMG - mario@dcc.ufmg.br
* Erickson Rangel do Nascimento - Advisor - UFMG - erickson@dcc.ufmg.br

### Institution ###

Federal University of Minas Gerais (UFMG)  
Computer Science Department  
Belo Horizonte - Minas Gerais -Brazil 

### Laboratory ###

![VeRLab](https://www.dcc.ufmg.br/dcc/sites/default/files/public/verlab-logo.png)

**VeRLab:** Laboratory of Computer Vision and Robotics   
https://www.verlab.dcc.ufmg.br

## Dataset ##

DoMSEV is an 80-hour dataset of multimodal (RGB-D, IMU, and GPS) semantic egocentric videos that covers a wide range of activities. You can get more info and download the dataset in the following page: 

* [DoMSEV – Dataset of Multimodal Semantic Egocentric Video](https://www.verlab.dcc.ufmg.br/semantic-hyperlapse/cvpr2018-dataset/).

![DoMSEV](../doc/DoMSEV.png)

## Code ##

### Dependencies ###

* MATLAB 2016a
* OpenCV 2.4 _(Tested with 2.4.9 and 2.4.13)_  
* Doxygen 1 _(for documentation only - Tested with 1.8.12)_  
* _Check the [MIFF](https://github.com/verlab/SemanticFastForward_JVCI_2018) code dependencies if you want to run the egocentric video stabilizer._

### Usage ###

**Before running the following steps, please compile the Optical Flow Estimator, the Accelerated Video Stabilizer and the Darknet. To compile the Optical Flow Estimator, go back to the project's main folder and execute step #1. To compile the Accelerated Video Stabilizer, go to the MIFF folder and execute step #7. To compile the Darknet, execute step #4 on the project's main folder and download the weights run (last thing on Darknet step) into the [_Darknet](../_Darknet) folder**

If you don't want to read all the steps, feel free to use the **Quick Guide**. To see it, execute the first step and click on *Help Index* in the *Help* menu.

1.  **Running the Code:**

	Into the _PythonScripts_ directory, run the following command:
```
 user@computer:<project_path/PythonScripts>: python main.py
```

2. **Selecting the Video:**
	
	On the main screen, click on *OpenFile* in the *File* menu. Then select the video that you want to accelerate.
```
 The valid formats are: ".mp4" and ".avi"
```

3. **Choosing the Semantic Extractor**:

	After selecting the video, choose the semantic extractor that you want for your video. The extractors available are: _face_ and _pedestrian_.

4. **Choosing the SpeedUp:**

	After selecting the video, choose the speed-up that you want to apply.
```
 The speed-up rate needs to be an integer greater than 1.
```

5. **Speeding-Up the Video:**
	
	After setting everything, click on the `Speed Up and Stabilize` button and check the progress on the screen that'll be opened.