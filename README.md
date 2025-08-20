#TriggeredbyScreenandAction

##프로그램 설명
화면의 특정 영역을 모니터링하고, 해당 영역에서 사전에 정해둔 템플릿 이미지를 인식하면 지정된 매크로를 실행하는 프로그램입니다.
애드 센스 끄기 귀찮아서 만들었습니다.

##설치 방법

###1단계
pip install PyQt5 pywin32 keyboard opencv-python numpy pyautogui
을 터미널에서 실행합니다.


###2단계
트리거가 될 이미지를 캡쳐해서 templates 폴더에 넣으십시오.
-사실 꼭 templates 폴더에 넣을 필요는 없지만, 업데이트 대비용입니다.

###3단계
main.py가 있는 폴더에서 터미널로 python main.py를 실행하십시오.
GUI가 실행되어야 합니다.

###4단계
GUI가 나오면, 
1)목표 윈도우를 설정하고, 
2)목표 윈도우에서 감시할 영역을 선택하고, 
3)해당 영역에서 나타나면 반응할 템플릿 이미지(아까 templates 폴더에 저장하라고 한 거)를 선택하고, 
4)해당 트리거에 반응해서 할 동작을 선택하십시오.

참고로 반응에 따른 동작은 다음과 같습니다.
클릭:트리거가 되는 이미지를 클릭합니다.
드래그(미구현):목표 윈도우 정중앙을 기준으로 드래그
스크롤(미구현):목표 윈도우 정중앙을 기준으로 스크롤

##사용된 주요 라이브러리 (Third-Party Libraries)

이 프로그램은 다음 파이썬 라이브러리를 사용합니다:

PyQt5
(GPL v3)
pywin32
(PSF License)
keyboard
(MIT License)
opencv-python
(Apache License 2.0)
numpy
(BSD License)
pyautogui
(BSD License)

##라이선스 (License)

이 프로젝트는 GPL v3 라이선스
를 따릅니다.

##연락처 (Contact)

Maintainer: pinakes1111
Email: pinakes1111@gmail.com

##개발 계획
대대적인 개편 예정임. 클래스 관리 같은 것도 정리하고, 기능도 많이 추가할 예정임.
