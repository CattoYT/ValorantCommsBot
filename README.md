# ValorantCommsBot

A valorant bot that can be used to automate communications using voice clips from different games.
This was written because I was bored + inspiration from SociallyIneptWeeb

This bot was partially written because I hate talking in VC with random people, so why not spend half a year making a program to do it for me?
I guess other socially inept (haha) people can use it too, so win win?

As of writing, Python 3.13 isn't out, but will be within the year. I plan on migrating quickly due to the lack of the GIL, which will significantly improve this app's performance currently.
This is mainly to clean up the shitty multiprcessing code i've written, and will hopefully be faster when starting up different modules such as the EnemyManager. When this happens, it will definitely take a massive refactor tho lol


Fun note: Google colab doesn't seem to allow me to change the save directory when exporting ipynbs   
A lot of ipynbs will be in the root directory for now, but they will be moved eventually (they wont probably)

# Setup:

Run the following (ideally in a venv):
```
pip install -r requirements.txt
```

EnemyManager currently makes use of [YOLOv5](https://github.com/ultralytics/yolov5) models from [Leaf48](https://github.com/Leaf48/YOLO-Models-For-Valorant/tree/main/Yolov5/YOLOv5s)
Please move them into this root folder and make sure the name matches in the torch.hub.load call in EnemyManager.py.
This will be a thing until my model finishes training and I will be providing that as default in this repo!

Some redundant code will be present, so just comment it out if you don't want to use it. I recommend commenting EnemyManager in main.py for a somewhat decent (yet small) release.


## Acknowledgements

- [YOLOv5](https://github.com/ultralytics/yolov5) by Ultralytics
  - License: AGPL v3.0
  
- [YOLOv8](https://github.com/ultralytics/ultralytics) by Ultralytics
  - License: AGPL v3.0

- [PyO3](https://github.com/PyO3/pyo3) 
  - License: MIT License

- [PyTorch](https://pytorch.org/)
  - License: BSD-3-Clause

- [OpenCV](https://opencv.org/)
  - License: Apache License 2.0

- [Tesseract](https://github.com/tesseract-ocr/tesseract) by Tesseract OCR
  - License: Apache License 2.0

Snake case stuff is often from AI, but not always, so thanks github copilot <3


# Disclaimer + Legal Stuff


*All voice clips copyright to their respective owner(s). This project does not claim 
ownership of any of the voice clips used in this project unless stated otherwise. 
This project does not knowingly intend or attempt to offend or violate any 
copyright or intellectual property rights of any entity. Some audio used on this 
project are taken from the web and believed to be in the public domain. In addition, 
to the best of this project's knowledge, all content is being used in compliance with the Fair Use Doctrine (Copyright Act of 1976, 
17 U.S.C. § 107.)The voice clips are provided for comment/criticism/news reporting/
educational purposes only.


Where every care has been taken to ensure the accuracy of the contents of this 
project, we do not warrant its completeness, quality and accuracy, nor can we 
guarantee that it is up-to-date. We will not be liable for any consequences 
arising from the use of, or reliance on, the contents of this project. The 
respective owners are exclusively responsible for external websites. This 
project accepts no liability of the content of external links.


Our project follows the safe harbor provisions of 17 U.S.C. §512, otherwise 
known as Digital Millennium Copyright Act (“DMCA”).


If any audio posted here are in violation of copyright law, please contact 
us and we will gladly remove the offending clips immediately upon receipt 
of valid proof of copyright infringement.
