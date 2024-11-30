import cv2
from config.settings import (
    SCREEN_HEIGHT, SCREEN_WIDTH, WEBCAM_DISPLAY_SIZE,
    CURSOR_COLOR, CURSOR_SIZE
)


class Visualizer:
    def __init__(self):
        self.window_name = 'Desktop Control with Hand Tracking'

    def prepare_display(self, desktop_frame, webcam_frame):
        """디스플레이 프레임 준비"""
        # 웹캠 화면 크기 조정
        webcam_small = cv2.resize(webcam_frame, WEBCAM_DISPLAY_SIZE)
        h, w = webcam_small.shape[:2]

        # 웹캠 화면을 우하단에 표시
        desktop_frame[
        SCREEN_HEIGHT - h:SCREEN_HEIGHT,
        SCREEN_WIDTH - w:SCREEN_WIDTH
        ] = webcam_small

        return desktop_frame

    def draw_cursor(self, frame, x, y):
        """커서 표시"""
        cv2.circle(frame, (x, y), CURSOR_SIZE, CURSOR_COLOR, -1)

    def draw_status(self, frame, is_clicking, scroll_direction=None):
        """상태 표시"""
        if is_clicking:
            cv2.putText(frame, "Pinching", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if scroll_direction:
            cv2.putText(frame, f"Scrolling {scroll_direction}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    def show_frame(self, frame):
        """프레임 표시"""
        cv2.imshow(self.window_name, frame)

    def cleanup(self):
        """창 정리"""
        cv2.destroyAllWindows()