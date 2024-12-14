# settings.py

# Screen settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Visualization settings
SKELETON_WIDTH = int(SCREEN_WIDTH / 8)     # 240px
SKELETON_HEIGHT = int(SCREEN_HEIGHT / 4)    # 270px
AREA_HEIGHT = int(SKELETON_HEIGHT / 3)      # 90px

# Box settings
BOX_PADDING = 10
BOX_THICKNESS = 2

# Colors
SCROLL_UP_COLOR = (0, 255, 0)     # 초록색
MOUSE_AREA_COLOR = (255, 255, 0)  # 노란색
SCROLL_DOWN_COLOR = (0, 255, 0)   # 초록색
SKELETON_COLOR = (0, 255, 0)      # 초록색
SKELETON_THICKNESS = 2

# Gesture settings
TAP_THRESHOLD = 0.145      # 엄지-중지 탭 인식 임계값
SCROLL_SPEED = 50         # 스크롤 속도

# Movement settings
MOVEMENT_SMOOTHING = 0.5   # 마우스 이동 보간 계수
COORDINATE_STABILITY = 0.8 # 좌표 안정화 계수
CLICK_STABILIZE_TIME = 0.1 # 클릭 시 좌표 고정 시간

# Debug
DEBUG_MODE = True