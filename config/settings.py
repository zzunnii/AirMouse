# settings.py
# Screen settings
# Screen settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# 고정된 400x400 크기의 스켈레톤 창
SKELETON_WIDTH = 200
SKELETON_HEIGHT = 200

BOX_PADDING = 40  # 고정된 40px 패딩
MOUSEPAD_MARGIN = 60  # 고정된 60px 마우스패드 여백

BOX_THICKNESS = 2
SKELETON_THICKNESS = 2

# Colors
BOX_COLOR = (0, 255, 0)  # 바운딩 박스 색상
MOUSEPAD_COLOR = (255, 255, 255)  # 마우스패드 영역 색상
SKELETON_COLOR = (0, 255, 0)


# 마우스/제스처 감도 설정
COORDINATE_STABILITY = 0.4   # 좌표 안정성 (0.8 -> 0.6)
TAP_THRESHOLD = 0.05        # 탭 인식 임계값 (0.145 -> 0.13)
SCROLL_SPEED = 50         # 스크롤 속도


# Mouse settings
CLICK_STABILIZE_TIME = 0.08  # 클릭 시 좌표 고정 시간

# Debug
DEBUG_MODE = True

# 마우스패드 영역 설정 (스켈레톤 창 내부의 비율)
MOUSEPAD_THICKNESS = 1  # 마우스패드 경계선 두께

# 마우스 감도 설정
MOUSE_SENSITIVITY = 15.0  # 감도 증가
MOVEMENT_SMOOTHING = 1.0  # 부드러움 감소로 반응성 향상