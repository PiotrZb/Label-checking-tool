# **Label checking tool**

## Description

Label validation tool written in python.<br />
The script draws bounding boxes on corresponding images and enables users to navigate through the dataset easily using the keyboard.<br />
Images not related to any label are automaticaly send to incorrect data folderd, as are labels.<br />
Supported image formats: .png, .jpg, .jpeg, .bmp.<br />
Labels schould be stored in .txt files in YOLO format.

## Requirements

You need to install opencv library for python:
```cmd
pip install opencv-python
```

## Usage

You can drop check_labels.py in folder containing your data (both images and labels) and run it via console:
```cmd
python check_labels.py 
```

Youn can also send args containing paths to images, labels, incorrect data folder and image format.
```cmd
python check_labels.py -ip ./images/ -lp ./labels/ -icp ./IncorrectData/ -if .png
```

## Keybinding

* Next image <kbd>d</kbd>
* Previous image <kbd>a</kbd>
* Send to incorrect data folder <kbd>Space</kbd>
* Quit <kbd>q</kbd>

## Default parameters

* Path to labels: './'
* Path to images: './'
* Path to incorrect data folder: './IncorrectData/'
* Image format: '.png'
* Size of displayed image: 1280x736
* Labels format: '.txt'
