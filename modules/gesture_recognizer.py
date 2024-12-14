import time
import numpy as np
from utils.math_utils import calculate_distance
from config.settings import (
    TAP_THRESHOLD, COORDINATE_STABILITY,
    CLICK_STABILIZE_TIME, AREA_HEIGHT,
    SKELETON_HEIGHT
)


class GestureRecognizer:
    def __init__(self):
        # 탭 관련 변수
        self.last_tap_time = 0
        self.tap_count = 0
        self.is_tapping = False
        self.tap_start_time = None
        self.tap_position = None
        self.is_dragging = False

        # 좌표 안정화를 위한 변수
        self.stable_position = None
        self.position_lock_time = None
        self.last_positions = []  # 최근 위치 기록 (평균 계산용)
        self.MAX_POSITIONS = 5  # 평균 계산에 사용할 위치 개수

        # 시간 설정
        self.TAP_COOLDOWN = 0.3  # 연속 탭 간격
        self.DOUBLE_TAP_TIME = 0.5  # 더블 탭 인식 시간
        self.DRAG_THRESHOLD = 0.5  # 드래그 인식을 위한 탭 유지 시간

    def check_index_finger_up(self, hand_landmarks):
        """검지 손가락이 펴져있는지 확인"""
        index_tip = hand_landmarks.landmark[8]  # 검지 끝
        index_pip = hand_landmarks.landmark[6]  # 검지 중간 마디 (PIP)
        index_mcp = hand_landmarks.landmark[5]  # 검지 시작 마디 (MCP)

        # 다른 손가락들의 끝 마디
        other_fingers_tips = [
            hand_landmarks.landmark[12],  # 중지 끝
            hand_landmarks.landmark[16],  # 약지 끝
            hand_landmarks.landmark[20]  # 소지 끝
        ]

        # 검지가 펴져있는지 확인
        is_index_extended = (index_tip.y < index_pip.y < index_mcp.y)

        # 다른 손가락들이 접혀있는지 확인
        are_others_folded = all(finger.y > index_pip.y for finger in other_fingers_tips)

        return is_index_extended and are_others_folded

    def get_stabilized_position(self, current_pos):
        """좌표 안정화"""
        self.last_positions.append(current_pos)
        if len(self.last_positions) > self.MAX_POSITIONS:
            self.last_positions.pop(0)

        # 평균 위치 계산
        avg_pos = np.mean(self.last_positions, axis=0)

        # 현재 위치와 평균 위치를 보간
        if self.stable_position is None:
            self.stable_position = avg_pos
        else:
            self.stable_position = (
                    self.stable_position * COORDINATE_STABILITY +
                    avg_pos * (1 - COORDINATE_STABILITY)
            )

        return self.stable_position

    def check_thumb_middle_tap(self, hand_landmarks):
        """엄지와 중지 손가락의 탭 동작 확인"""
        thumb_tip = hand_landmarks.landmark[4]
        middle_pip = hand_landmarks.landmark[11]  # 중지 두번째 마디
        return calculate_distance(thumb_tip, middle_pip) < TAP_THRESHOLD

    def get_area_type(self, y_coord):
        """현재 손가락이 위치한 영역 확인"""
        relative_y = y_coord * SKELETON_HEIGHT
        if relative_y < AREA_HEIGHT:
            return "SCROLL_UP"
        elif relative_y > 2 * AREA_HEIGHT:
            return "SCROLL_DOWN"
        return "MOUSE"

    def update_gesture_state(self, hand_landmarks):
        """제스처 상태 업데이트 및 동작 결정"""
        if not self.check_index_finger_up(hand_landmarks):
            return None, None

        current_time = time.time()
        is_tapping_now = self.check_thumb_middle_tap(hand_landmarks)

        # 현재 포인터 위치 (검지 끝)
        current_pos = np.array([
            hand_landmarks.landmark[8].x,
            hand_landmarks.landmark[8].y
        ])

        # 영역 확인
        area_type = self.get_area_type(current_pos[1])
        if area_type in ["SCROLL_UP", "SCROLL_DOWN"]:
            return area_type, current_pos

        # 탭 동작 처리
        if is_tapping_now and not self.is_tapping:
            # 새로운 탭 시작
            if current_time - self.last_tap_time < self.DOUBLE_TAP_TIME:
                self.tap_count += 1
            else:
                self.tap_count = 1

            self.tap_start_time = current_time
            self.last_tap_time = current_time
            self.position_lock_time = current_time
            self.tap_position = self.get_stabilized_position(current_pos)

        elif is_tapping_now and self.is_tapping:
            # 드래그 시작
            if not self.is_dragging and \
                    current_time - self.tap_start_time > self.DRAG_THRESHOLD:
                self.is_dragging = True
                return "DRAG", self.tap_position

        elif not is_tapping_now and self.is_tapping:
            # 탭 종료
            gesture_result = None
            if self.is_dragging:
                self.is_dragging = False
                gesture_result = ("DROP", self.tap_position)
            elif self.tap_count == 2:
                self.tap_count = 0
                gesture_result = ("CLICK", self.tap_position)
            else:
                gesture_result = ("SELECT", self.tap_position)

            # 상태 초기화
            self.tap_position = None
            self.tap_start_time = None
            self.is_tapping = False
            return gesture_result

        self.is_tapping = is_tapping_now
        return None, self.get_stabilized_position(current_pos)