import math
import time
import numpy as np
from utils.math_utils import calculate_distance
from config.settings import (
    TAP_THRESHOLD, COORDINATE_STABILITY,
    CLICK_STABILIZE_TIME,
    SKELETON_HEIGHT, DEBUG_MODE
)


class GestureRecognizer:
    def __init__(self):
        # 탭 관련 변수
        self.is_tapping = False
        self.tap_start_time = None
        self.tap_position = None
        self.is_dragging = False

        # 좌표 안정화를 위한 변수
        self.stable_position = None
        self.last_positions = []  # 최근 위치 기록 (평균 계산용)
        self.MAX_POSITIONS = 5  # 평균 계산에 사용할 위치 개수

        # 시간 설정
        self.DRAG_THRESHOLD = 0.3  # 드래그 인식을 위한 탭 유지 시간 (300ms)

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

    def check_scroll_up(self, hand_landmarks):
        """엄지, 검지, 중지가 모두 펴졌는지 확인"""
        thumb_tip = hand_landmarks.landmark[4]  # 엄지 끝
        thumb_mcp = hand_landmarks.landmark[2]  # 엄지 마디
        index_tip = hand_landmarks.landmark[8]  # 검지 끝
        index_pip = hand_landmarks.landmark[6]  # 검지 중간 마디
        middle_tip = hand_landmarks.landmark[12]  # 중지 끝
        middle_pip = hand_landmarks.landmark[10]  # 중지 중간 마디

        # 각 손가락이 펴져있는지 확인
        thumb_extended = thumb_tip.y < thumb_mcp.y
        index_extended = index_tip.y < index_pip.y
        middle_extended = middle_tip.y < middle_pip.y

        return thumb_extended and index_extended and middle_extended

    def check_scroll_down(self, hand_landmarks):
        """엄지만 펴지고 나머지는 접혀있는지 확인"""
        thumb_tip = hand_landmarks.landmark[4]  # 엄지 끝
        thumb_mcp = hand_landmarks.landmark[2]  # 엄지 마디
        index_tip = hand_landmarks.landmark[8]  # 검지 끝
        index_pip = hand_landmarks.landmark[6]  # 검지 중간 마디
        middle_tip = hand_landmarks.landmark[12]  # 중지 끝
        middle_pip = hand_landmarks.landmark[10]  # 중지 중간 마디

        # 엄지는 펴져있고 나머지는 접혀있는지 확인
        thumb_extended = thumb_tip.y < thumb_mcp.y
        index_folded = index_tip.y > index_pip.y
        middle_folded = middle_tip.y > middle_pip.y

        return thumb_extended and index_folded and middle_folded

    def check_index_finger_tap(self, hand_landmarks):
        """검지 손가락만 펴져있는지 확인하는 개선된 버전"""
        # 손가락 랜드마크 포인트
        thumb_tip = hand_landmarks.landmark[4]  # 엄지 끝
        thumb_mcp = hand_landmarks.landmark[2]  # 엄지 밑 마디

        index_tip = hand_landmarks.landmark[8]  # 검지 끝
        index_pip = hand_landmarks.landmark[6]  # 검지 중간 마디
        index_mcp = hand_landmarks.landmark[5]  # 검지 밑 마디

        middle_tip = hand_landmarks.landmark[12]  # 중지 끝
        middle_pip = hand_landmarks.landmark[10]  # 중지 중간 마디

        ring_tip = hand_landmarks.landmark[16]  # 약지 끝
        ring_pip = hand_landmarks.landmark[14]  # 약지 중간 마디

        pinky_tip = hand_landmarks.landmark[20]  # 소지 끝
        pinky_pip = hand_landmarks.landmark[18]  # 소지 중간 마디

        # 1. 검지가 확실히 펴져있는지 확인
        is_index_extended = (
                index_tip.y < index_pip.y - 0.02 and  # 임계값 추가
                index_pip.y < index_mcp.y
        )

        # 2. 다른 손가락들이 확실히 접혀있는지 확인
        are_others_folded = (
                middle_tip.y > middle_pip.y + 0.02 and  # 중지
                ring_tip.y > ring_pip.y + 0.02 and  # 약지
                pinky_tip.y > pinky_pip.y + 0.02  # 소지
        )

        # 3. 엄지가 접혀있는지 확인 (옆에서 보이는 형태)
        is_thumb_folded = (
                abs(thumb_tip.z - thumb_mcp.z) < 0.05 and  # z축 차이가 작음
                thumb_tip.x > thumb_mcp.x  # 엄지가 안쪽으로
        )

        if DEBUG_MODE:
            print(f"Index extended: {is_index_extended}")
            print(f"Others folded: {are_others_folded}")
            print(f"Thumb folded: {is_thumb_folded}")

        # 모든 조건을 만족해야 함
        return is_index_extended and are_others_folded and is_thumb_folded

    def update_gesture_state(self, hand_landmarks):
        """제스처 상태 업데이트 및 동작 결정"""
        current_time = time.time()
        is_tapping_now = self.check_index_finger_tap(hand_landmarks)

        # 현재 포인터 위치
        current_pos = np.array([
            hand_landmarks.landmark[8].x,
            hand_landmarks.landmark[8].y
        ])

        # 위치 안정화
        stabilized_pos = self.get_stabilized_position(current_pos)

        # 탭 동작 처리 (1 만들기)
        if is_tapping_now and not self.is_tapping:
            # 새로운 탭 시작
            self.tap_start_time = current_time
            self.tap_position = stabilized_pos
            self.is_tapping = True
            return ("CLICK", stabilized_pos)

        elif not is_tapping_now and self.is_tapping:
            # 탭 종료
            self.is_tapping = False
            if self.is_dragging:
                self.is_dragging = False
                return ("DROP", self.tap_position)

            self.tap_position = None
            return (None, stabilized_pos)

        elif is_tapping_now and self.is_tapping:
            # 1을 유지한 채로 이동하면 드래그
            if not self.is_dragging and current_time - self.tap_start_time > self.DRAG_THRESHOLD:
                self.is_dragging = True
                return ("DRAG", self.tap_position)
            return (None, self.tap_position)

        # 기본 상태 (1이 아닌 상태로 움직일 때)
        return (None, stabilized_pos)