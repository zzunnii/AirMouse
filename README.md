# 현재 클릭 및 이동 반응성 이슈로 불안정한 프로그램

# Virtual Mouse with Hand Gesture
> 손 제스처를 이용한 가상 마우스 제어 시스템

## 📹실행 장면
스크롤은 완벽한 기능을 보이지만, 이동과 클릭의 오류가 자주 발생

### 클릭 


https://github.com/user-attachments/assets/91ed0449-2cfd-4399-afe6-e1bf84546936


### 스크롤 


https://github.com/user-attachments/assets/0a089241-812c-43dd-980d-d589b9067bf4


## ✨ 주요 기능
- 손 제스처를 통한 마우스 커서 제어
- 엄지-중지 탭 동작을 통한 클릭/드래그 기능
- 엄지/검지/중지를 이용한 스크롤
- 실시간 손 스켈레톤 시각화

## 🔧 시스템 요구사항
- Python 3.8+
- OpenCV
- MediaPipe 
- PyAutoGUI
- NumPy

## 📦 설치 방법
```bash
# 저장소 클론
git clone [repository URL]

# 필요 패키지 설치  
pip install -r requirements.txt
```

----

## 🚀 실행 방법
python main.py

## 🗂 모듈 구조
```
├── config/
│   └── settings.py         # 환경 설정
├── modules/
│   ├── hand_tracker.py     # 손 인식 및 추적
│   ├── gesture_recognizer.py # 제스처 인식
│   └── mouse_controller.py   # 마우스 제어  
├── utils/
│   └── math_utils.py       # 수학 유틸리티
└── main.py                 # 메인 실행 파일
```

## 👋 제스처 가이드

### 마우스 이동: 검지 손가락으로 포인팅
![스크린샷 2024-12-15 160923](https://github.com/user-attachments/assets/f7f83ab7-c93b-4d3a-a0ec-e280e02de1d0)

### 클릭: 검지 손가락으로 1
![스크린샷 2024-12-15 160957](https://github.com/user-attachments/assets/26a2ded4-6f4d-4938-bb03-f42c8ca2e400)

### 드래그: 1을 유지

### 스크롤:
### 위로: 엄지, 검지, 중지 펴기
![스크린샷 2024-12-15 161008](https://github.com/user-attachments/assets/d02a91cf-e498-4581-a128-61f3a62a3455)

### 아래로 : 검지, 중지, 접고 엄지만 펴기
![스크린샷 2024-12-15 161017](https://github.com/user-attachments/assets/8e94a8d9-1247-45d3-99b8-5ff5ae515d8f)


## 🔜 향후 계획

 더 많은 제스처 추가
 성능 최적화
 설정 GUI 추가

## 🤝 기여하기
버그 리포트나 새로운 기능 제안은 이슈를 통해 제출해주세요.

tjdwns7488@gmail.com

---

##📝 Beta v1.0 업데이트 내역

UI 개선

스켈레톤 창 크기를 화면 1/10 크기로 조정
단일 바운딩 박스로 단순화


제스처 개선

영역 기반 스크롤을 손가락 제스처로 변경
엄지-중지 탭 인식 개선
중요 포인트(엄지 끝, 중지 두번째 마디) 시각적 강조


마우스 제어 개선

마우스패드 방식의 상대적 이동 구현
작은 영역으로 전체 화면 커버 가능
좌표 보정/지연 제거로 즉각적인 반응
