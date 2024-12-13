import cv2
from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SKELETON_WIDTH,
    SKELETON_HEIGHT,
    BOX_PADDING
)


class Visualizer:
    def __init__(self):
        # 우측 하단에 고정할 스켈레톤 창의 위치와 크기
        self.skeleton_width = SKELETON_WIDTH
        self.skeleton_height = SKELETON_HEIGHT
        self.skeleton_x = SCREEN_WIDTH - self.skeleton_width - 20
        self.skeleton_y = SCREEN_HEIGHT - self.skeleton_height - 20

        # 바운딩 박스 영역 정의
        self.box_padding = BOX_PADDING
        self.box_x = self.skeleton_x - self.box_padding
        self.box_y = self.skeleton_y - self.box_padding
        self.box_width = self.skeleton_width + (self.box_padding * 2)
        self.box_height = self.skeleton_height + (self.box_padding * 2)

    def draw_bounding_box(self, frame):
        """바운딩 박스 그리기"""
        cv2.rectangle(frame,
                      (self.box_x, self.box_y),
                      (self.box_x + self.box_width, self.box_y + self.box_height),
                      (255, 0, 0), 2)

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