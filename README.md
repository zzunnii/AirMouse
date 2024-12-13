#ReadMe 수정 중 아직 실행 안됨

# Hand Gesture Mouse Control System
> 손 제스처를 통해 마우스를 제어하는 시스템

[영상 데모 위치]

## ✨ 주요 기능
- 손 제스처를 통한 마우스 커서 제어
- 핀치(엄지-검지 집기) 제스처로 클릭 동작 수행  
- 핀치 후 유지를 통한 스크롤 모드 전환
- 주먹 쥐었다 펴기로 엔터키 입력
- 투명 오버레이를 통한 실시간 손 스켈레톤 시각화
- 음성 인식을 통한 부가 기능 (실험적 기능)

## 🔧 시스템 요구사항
- Python 3.8+
- OpenCV
- MediaPipe 
- PyAutoGUI
- PyQt5
- Transformers (음성인식 기능 사용시)
- Speech Recognition (음성인식 기능 사용시)

## 📦 설치 방법
```bash
# 저장소 클론
git clone [repository URL]

# 필요 패키지 설치  
pip install -r requirements.txt
```
## 🚀 실행 방법
python main.py

[실행 화면 스크린샷 들어갈 예정]

## 🗂 모듈 구조
├── config/
│   └── settings.py         # 환경 설정
├── modules/
│   ├── hand_tracker.py     # 손 인식 및 추적
│   ├── gesture_recognizer.py # 제스처 인식
│   ├── mouse_controller.py   # 마우스 제어  
│   ├── overlay_window.py     # 투명 오버레이 창
│   ├── visualization.py      # 시각화
│   └── voice_recognizer.py   # 음성 인식 (실험적)
├── utils/
│   └── math_utils.py       # 수학 유틸리티
└── main.py                 # 메인 실행 파일

## 👋 제스처 가이드
[제스처 설명 이미지 들어갈 예정]

마우스 이동: 검지 손가락으로 포인팅
클릭: 엄지와 검지로 핀치 동작 후 빠르게 펴기
스크롤: 핀치 동작을 유지하고 손을 상하로 이동
엔터키: 주먹을 쥐었다 빠르게 펴기

## ⚙️ 설정 커스터마이징
config/settings.py에서 다음 설정들을 조정할 수 있습니다:

화면 해상도
웹캠 해상도
제스처 인식 감도
마우스 이동 감도
시각화 설정

## 🐛 알려진 이슈
밝기가 너무 어두운 환경에서 인식률 저하
복잡한 배경에서 가끔 오인식 발생
[기타 이슈들...]

## 🔜 향후 계획
 다중 손 인식 지원
 추가 제스처 매핑 기능
 설정 GUI 추가
 성능 최적화

## 🤝 기여하기
버그 리포트나 새로운 기능 제안은 이슈를 통해 제출해주세요.
풀 리퀘스트는 다음 가이드라인을 따라주세요:

새로운 브랜치 생성
테스트 코드 포함
문서화 포함

## 📜 라이선스
[실제 사용 영상 위치]

## 💬 문의
이메일: [이메일 주소]
이슈 트래커: [이슈 트래커 URL]

##🙏 크레딧
MediaPipe
OpenCV
[기타 사용된 라이브러리들...]

