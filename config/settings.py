# Screen settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Webcam settings
WEBCAM_WIDTH = 640  # 추가
WEBCAM_HEIGHT = 480  # 추가

# Gesture settings
PINCH_THRESHOLD = 0.05  # 핀치 동작 인식을 위한 임계값
PINCH_COOLDOWN = 0.3    # 연속 핀치 간격
DOUBLE_CLICK_TIME = 0.5  # 더블클릭 인식 시간
DRAG_THRESHOLD = 0.5    # 드래그 인식을 위한 핀치 유지 시간
DISTANCE_CHANGE_THRESHOLD = 0.03  # 핀치 의도 감지를 위한 거리 변화율 임계값

# Mouse settings
MOUSE_SMOOTHING = 0.5  # 마우스 움직임 보간 계수 (0~1)

# Visualization settings
SKELETON_WIDTH = 300  # 스켈레톤 창 너비
SKELETON_HEIGHT = 200  # 스켈레톤 창 높이
BOX_PADDING = 20  # 바운딩 박스 여백

# Colors & Style
SKELETON_COLOR = (0, 255, 0)  # 스켈레톤 선 색상 (녹색)
SKELETON_THICKNESS = 2  # 스켈레톤 선 두께
BOX_COLOR = (0, 255, 0)  # 바운딩 박스 색상 (녹색)
BOX_THICKNESS = 2  # 바운딩 박스 선 두께

#시간 관련 상수
HOVER_CLICK_DELAY = 1.0  # 자동 클릭을 위한 호버 시간
POSITION_LOCK_TIME = 0.3  # 핀치를 위한 위치 고정 시간
MOVEMENT_THRESHOLD = 5  # 마우스 이동 감지를 위한 픽셀 임계값