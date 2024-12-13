import time
from utils.math_utils import calculate_distance
from config.settings import PINCH_THRESHOLD


class GestureRecognizer:
    def __init__(self):
        # 핀치 관련 변수
        self.last_pinch_distance = None
        self.last_distance_time = None
        self.distance_history = []  # 거리 변화 추적용
        self.intent_detected_position = None  # 핀치 의도가 감지된 시점의 위치
        self.last_click_time = 0  # 더블클릭 감지용
        self.click_count = 0  # 클릭 횟수
        self.is_dragging = False  # 드래그 상태
        self.was_clicking = False
        self.pinch_start_time = None

        # 시간 설정
        self.PINCH_COOLDOWN = 0.3  # 연속 핀치 간격
        self.DOUBLE_CLICK_TIME = 0.5  # 더블클릭 인식 시간
        self.DRAG_THRESHOLD = 0.5  # 드래그 인식을 위한 핀치 유지 시간
        self.DISTANCE_CHANGE_THRESHOLD = 0.03  # 핀치 의도 감지를 위한 거리 변화율 임계값

    def is_pinching(self, hand_landmarks):
        """엄지와 검지 손가락이 핀치 동작을 하고 있는지 확인"""
        thumb_tip = hand_landmarks.landmark[4]  # 엄지 끝
        index_tip = hand_landmarks.landmark[8]  # 검지 끝
        return calculate_distance(thumb_tip, index_tip) < PINCH_THRESHOLD

    def calculate_distance_change_rate(self, current_distance, current_time):
        """거리 변화율 계산"""
        if self.last_pinch_distance is None or self.last_distance_time is None:
            self.last_pinch_distance = current_distance
            self.last_distance_time = current_time
            return 0

        time_diff = current_time - self.last_distance_time
        if time_diff == 0:
            return 0

        distance_change = self.last_pinch_distance - current_distance
        change_rate = distance_change / time_diff

        self.last_pinch_distance = current_distance
        self.last_distance_time = current_time

        return change_rate

    def detect_pinch_intent(self, hand_landmarks):
        """핀치 의도 감지"""
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        current_distance = calculate_distance(thumb_tip, index_tip)
        current_time = time.time()

        change_rate = self.calculate_distance_change_rate(current_distance, current_time)

        # 거리가 빠르게 줄어들기 시작하는 시점 감지
        if change_rate > self.DISTANCE_CHANGE_THRESHOLD and not self.intent_detected_position:
            self.intent_detected_position = (index_tip.x, index_tip.y)
            return True
        return False

    def update_gesture_state(self, hand_landmarks):
        """제스처 상태 업데이트 및 동작 결정"""
        current_time = time.time()
        is_pinching = self.is_pinching(hand_landmarks)

        # 핀치 의도 감지
        self.detect_pinch_intent(hand_landmarks)

        # 핀치 동작 처리
        if is_pinching and not self.was_clicking:
            # 새로운 핀치 시작
            if current_time - self.last_click_time < self.DOUBLE_CLICK_TIME:
                self.click_count += 1
            else:
                self.click_count = 1

            self.pinch_start_time = current_time
            self.last_click_time = current_time

        elif is_pinching and self.was_clicking:
            # 핀치 유지 중
            if current_time - self.pinch_start_time > self.DRAG_THRESHOLD:
                self.is_dragging = True
                return "DRAG", self.intent_detected_position

        elif not is_pinching and self.was_clicking:
            # 핀치 해제
            if self.is_dragging:
                self.is_dragging = False
                return "DROP", self.intent_detected_position
            elif self.click_count == 2:
                self.click_count = 0
                return "DOUBLE_CLICK", self.intent_detected_position
            else:
                return "CLICK", self.intent_detected_position

            self.intent_detected_position = None
            self.pinch_start_time = None

        self.was_clicking = is_pinching
        return None, None