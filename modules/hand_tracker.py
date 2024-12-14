import cv2
import mediapipe as mp
from config.settings import (
    SKELETON_COLOR, SKELETON_THICKNESS,
    SKELETON_WIDTH, SKELETON_HEIGHT
)


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.setup_webcam()

    def setup_webcam(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        results = self.hands.process(frame_rgb)
        frame_rgb.flags.writeable = True
        return results

    def draw_landmarks(self, frame, hand_landmarks):
        """스케일이 조정된 스켈레톤 그리기"""
        scale = 0.4  # 스켈레톤 크기를 40%로 축소

        # 스켈레톤 중심점 계산
        center_x = sum(lm.x for lm in hand_landmarks.landmark) / len(hand_landmarks.landmark)
        center_y = sum(lm.y for lm in hand_landmarks.landmark) / len(hand_landmarks.landmark)

        # 스케일이 적용된 랜드마크 그리기
        connections = self.mp_hands.HAND_CONNECTIONS
        for connection in connections:
            start_idx, end_idx = connection

            start = hand_landmarks.landmark[start_idx]
            end = hand_landmarks.landmark[end_idx]

            # 중심점 기준으로 스케일 조정
            start_x = int(((start.x - center_x) * scale + center_x) * frame.shape[1])
            start_y = int(((start.y - center_y) * scale + center_y) * frame.shape[0])
            end_x = int(((end.x - center_x) * scale + center_x) * frame.shape[1])
            end_y = int(((end.y - center_y) * scale + center_y) * frame.shape[0])

            cv2.line(frame, (start_x, start_y), (end_x, end_y),
                     SKELETON_COLOR, SKELETON_THICKNESS)

            # 중요 포인트만 강조
            if start_idx in [4, 11]:  # 엄지 끝과 중지 두번째 마디
                cv2.circle(frame, (start_x, start_y), 3, (0, 0, 255), -1)

    def cleanup(self):
        self.cap.release()