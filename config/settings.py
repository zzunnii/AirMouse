# settings.py
# Screen settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Visualization settings - 디스플레이 크기의 1/10
SKELETON_WIDTH = int(SCREEN_WIDTH / 10)   # 192px
SKELETON_HEIGHT = int(SCREEN_HEIGHT / 10)  # 108px

# Box settings
BOX_PADDING = int(SKELETON_WIDTH * 0.05)  # 창 크기의 5%
BOX_THICKNESS = 2
SKELETON_THICKNESS = 2

# Colors
BOX_COLOR = (0, 255, 0)  # 단일 바운딩 박스 색상
SKELETON_COLOR = (0, 255, 0)

# 마우스/제스처 감도 설정
MOVEMENT_SMOOTHING = 0.7     # 마우스 움직임 부드러움 (0.5 -> 0.7)
COORDINATE_STABILITY = 0.6   # 좌표 안정성 (0.8 -> 0.6)
TAP_THRESHOLD = 0.13        # 탭 인식 임계값 (0.145 -> 0.13)
SCROLL_SPEED = 50         # 스크롤 속도


# Mouse settings
CLICK_STABILIZE_TIME = 0.08  # 클릭 시 좌표 고정 시간

# Debug
DEBUG_MODE = True