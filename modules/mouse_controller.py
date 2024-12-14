import pyautogui
import time
from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SKELETON_WIDTH,
    SKELETON_HEIGHT,
    BOX_PADDING,
    MOUSE_SMOOTHING
)


class MouseController:
    def __init__(self):
        pyautogui.FAILSAFE = False

        # 화면 설정
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # 마우스 상태
        self.last_x = None
        self.last_y = None
        self.is_dragging = False

        # 좌표 보간을 위한 설정
        self.smoothing_factor = MOUSE_SMOOTHING

    def move_mouse(self, hand_landmark):
        """L자 포즈 기반 마우스 이동"""
        # 손의 좌표를 0-1 범위로 정규화된 값으로 변환
        rel_x = hand_landmark.x
        rel_y = hand_landmark.y

        # 정규화된 좌표를 스크린 좌표로 변환
        screen_x = rel_x * self.screen_width
        screen_y = rel_y * self.screen_height

        # 부드러운 움직임을 위한 보간
        if self.last_x is not None:
            screen_x = self.last_x + (screen_x - self.last_x) * self.smoothing_factor
            screen_y = self.last_y + (screen_y - self.last_y) * self.smoothing_factor

        # 화면 범위 제한
        screen_x = max(0, min(screen_x, self.screen_width))
        screen_y = max(0, min(screen_y, self.screen_height))

        self.last_x = screen_x
        self.last_y = screen_y

        # 마우스 이동
        pyautogui.moveTo(screen_x, screen_y, duration=0.05)
        return screen_x, screen_y

    def select(self, x=None, y=None):
        """항목 선택 (마우스 클릭)"""
        if x is not None and y is not None:
            pyautogui.click(x=x, y=y, button='left')
        else:
            pyautogui.click(button='left')

    def click(self, x=None, y=None):
        """더블 클릭"""
        if x is not None and y is not None:
            pyautogui.doubleClick(x=x, y=y)
        else:
            pyautogui.doubleClick()

    def start_drag(self, x=None, y=None):
        """드래그 시작"""
        if x is not None and y is not None:
            pyautogui.mouseDown(x=x, y=y, button='left')
        else:
            pyautogui.mouseDown(button='left')
        self.is_dragging = True

    def end_drag(self, x=None, y=None):
        """드래그 종료"""
        if self.is_dragging:
            if x is not None and y is not None:
                pyautogui.mouseUp(x=x, y=y, button='left')
            else:
                pyautogui.mouseUp(button='left')
            self.is_dragging = False

    def get_current_position(self):
        """현재 마우스 위치 반환"""
        return pyautogui.position()