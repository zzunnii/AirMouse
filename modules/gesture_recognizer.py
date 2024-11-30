import time
from utils.math_utils import calculate_distance
from config.settings import PINCH_THRESHOLD, SCROLL_THRESHOLD


class GestureRecognizer:
    def __init__(self):
        self.last_y = None
        self.was_clicking = False
        self.pinch_start_time = None
        self.scroll_mode = False
        self.SCROLL_ACTIVATION_TIME = 0.5  # 스크롤 모드로 전환되는 핀치 유지 시간 (초)
        self.last_fist_time = 0
        self.fist_gesture_cooldown = 0.5  # 주먹 제스처 쿨다운 시간 (초)
        self.fist_start_time = None
        self.last_gesture_was_fist = False

    def is_pinching(self, hand_landmarks):
        """엄지와 검지 손가락이 핀치 동작을 하고 있는지 확인"""
        thumb_tip = hand_landmarks.landmark[4]  # 엄지 끝
        index_tip = hand_landmarks.landmark[8]  # 검지 끝
        return calculate_distance(thumb_tip, index_tip) < PINCH_THRESHOLD

    def is_fist(self, hand_landmarks):
        """주먹을 쥐었는지 확인"""
        # 모든 손가락 끝과 중간 마디의 y좌표 비교
        fingers = [
            (8, 6),  # 검지
            (12, 10),  # 중지
            (16, 14),  # 약지
            (20, 18)  # 소지
        ]

        # 모든 손가락이 접혔는지 확인
        all_fingers_bent = all(
            hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y
            for tip, pip in fingers
        )

        return all_fingers_bent

    def detect_fist_and_release(self, hand_landmarks):
        """주먹을 쥐었다가 펴는 동작 감지"""
        current_time = time.time()
        is_fist_now = self.is_fist(hand_landmarks)

        # 쿨다운 체크
        if current_time - self.last_fist_time < self.fist_gesture_cooldown:
            return False

        if is_fist_now and not self.last_gesture_was_fist:
            # 주먹을 막 쥐기 시작한 시점
            self.fist_start_time = current_time
        elif not is_fist_now and self.last_gesture_was_fist:
            # 주먹을 편 시점
            if self.fist_start_time and (current_time - self.fist_start_time < 1.0):
                self.last_fist_time = current_time
                self.fist_start_time = None
                self.last_gesture_was_fist = False
                return True

        self.last_gesture_was_fist = is_fist_now
        return False

    def update_gesture_state(self, hand_landmarks):
        """제스처 상태 업데이트 및 동작 결정"""
        current_time = time.time()
        is_pinching_now = self.is_pinching(hand_landmarks)

        # 핀치 시작
        if is_pinching_now and not self.was_clicking:
            self.pinch_start_time = current_time
            self.scroll_mode = False

        # 핀치 유지 중
        elif is_pinching_now and self.was_clicking:
            if not self.scroll_mode and self.pinch_start_time and \
                    (current_time - self.pinch_start_time > self.SCROLL_ACTIVATION_TIME):
                self.scroll_mode = True

        # 핀치 해제
        elif not is_pinching_now and self.was_clicking:
            if not self.scroll_mode and self.pinch_start_time and \
                    (current_time - self.pinch_start_time <= self.SCROLL_ACTIVATION_TIME):
                # 클릭으로 처리
                return "CLICK"
            self.pinch_start_time = None
            self.scroll_mode = False

        self.was_clicking = is_pinching_now
        return "SCROLL" if self.scroll_mode else None

    def get_scroll_amount(self, hand_landmarks):
        """스크롤 양과 방향을 계산"""
        if self.last_y is None:
            self.last_y = hand_landmarks.landmark[8].y
            return 0

        current_y = hand_landmarks.landmark[8].y
        y_change = current_y - self.last_y
        self.last_y = current_y

        if abs(y_change) > SCROLL_THRESHOLD:
            return int(-y_change * 500)  # 스크롤 방향과 양 계산
        return 0

    def reset_scroll_state(self):
        """스크롤 상태 초기화"""
        self.last_y = None

    def update_click_state(self, is_clicking):
        """클릭 상태 업데이트 및 변화 감지"""
        changed = is_clicking != self.was_clicking
        self.was_clicking = is_clicking
        return changed