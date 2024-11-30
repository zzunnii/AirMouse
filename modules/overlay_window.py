from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
import cv2
import sys
import numpy as np


class OverlayWindow(QMainWindow):
    def __init__(self, hand_tracker, gesture_recognizer, mouse_controller):
        super().__init__()
        self.hand_tracker = hand_tracker
        self.gesture_recognizer = gesture_recognizer
        self.mouse_controller = mouse_controller

        # 투명 창 설정
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        # 전체 화면 크기로 설정
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # 마우스 이벤트 투과 설정
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 타이머 설정
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_overlay)
        self.timer.start(16)  # ~60fps

        self.landmarks = None
        self.current_gesture = None

    def update_overlay(self):
        # 웹캠 프레임 획득
        webcam_frame = self.hand_tracker.get_frame()
        if webcam_frame is None:
            return

        # 핸드 트래킹 수행
        results = self.hand_tracker.process_frame(webcam_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 제스처 인식 및 처리
                gesture = self.gesture_recognizer.update_gesture_state(hand_landmarks)

                # 엔터키를 위한 주먹 제스처 감지
                if self.gesture_recognizer.detect_fist_and_release(hand_landmarks):
                    self.mouse_controller.press_enter()

                # 제스처에 따른 동작 처리
                if gesture == "CLICK":
                    self.mouse_controller.click()
                elif gesture == "SCROLL":
                    scroll_amount = self.gesture_recognizer.get_scroll_amount(hand_landmarks)
                    if scroll_amount != 0:
                        self.mouse_controller.scroll(scroll_amount)
                else:
                    self.gesture_recognizer.reset_scroll_state()
                    # 마우스 이동
                    point = hand_landmarks.landmark[8]  # 검지 끝
                    cursor_x, cursor_y = self.mouse_controller.move_mouse(point)

                self.landmarks = hand_landmarks
                self.current_gesture = gesture
        else:
            self.landmarks = None
            self.current_gesture = None

        self.update()  # 화면 갱신

    def paintEvent(self, event):
        if not self.landmarks:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 스켈레톤 그리기
        painter.setPen(QPen(QColor(0, 255, 0), 2))

        connections = self.hand_tracker.mp_hands.HAND_CONNECTIONS
        landmarks = self.landmarks.landmark

        # 모든 연결선 그리기
        for connection in connections:
            start_idx, end_idx = connection
            start_point = landmarks[start_idx]
            end_point = landmarks[end_idx]

            start_x = int(start_point.x * SCREEN_WIDTH)
            start_y = int(start_point.y * SCREEN_HEIGHT)
            end_x = int(end_point.x * SCREEN_WIDTH)
            end_y = int(end_point.y * SCREEN_HEIGHT)

            painter.drawLine(start_x, start_y, end_x, end_y)

        # 현재 모드 표시
        if self.current_gesture:
            painter.setPen(QColor(255, 255, 255))
            text = "SCROLL" if self.current_gesture == "SCROLL" else "MOUSE"
            painter.drawText(100, 30, text)

    def keyPressEvent(self, event):
        # ESC 키로 종료
        if event.key() == Qt.Key_Escape:
            self.close()