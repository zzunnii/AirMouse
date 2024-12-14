import pyautogui
from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SKELETON_WIDTH,
    SKELETON_HEIGHT,
    BOX_PADDING
)


class MouseController:
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.sensitivity = 0.5  # 마우스 감도

    def move_mouse(self, hand_landmark):
        """손의 움직임을 마우스 커서의 속도로 변환"""
        # 현재 마우스 위치 가져오기
        current_x, current_y = pyautogui.position()

        # 손의 움직임을 속도로 변환
        move_x = hand_landmark.x * SKELETON_WIDTH * self.sensitivity
        move_y = hand_landmark.y * SKELETON_HEIGHT * self.sensitivity

        # 새로운 마우스 위치 계산
        new_x = current_x + int(move_x)
        new_y = current_y + int(move_y)

        # 화면 범위 제한
        new_x = max(0, min(new_x, self.screen_width))
        new_y = max(0, min(new_y, self.screen_height))

        # 마우스 이동
        pyautogui.moveTo(new_x, new_y)
        return new_x, new_y

    def select(self, x=None, y=None):
        """항목 선택 (마우스 클릭)"""
        pyautogui.click()

    def click(self, x=None, y=None):
        """더블 클릭"""
        pyautogui.doubleClick()

    def start_drag(self, x=None, y=None):
        """드래그 시작"""
        pyautogui.mouseDown()

    def end_drag(self, x=None, y=None):
        """드래그 종료"""
        pyautogui.mouseUp()

    def scroll(self, direction):
        """스크롤"""
        if direction == "UP":
            pyautogui.scroll(20)  # 위로 스크롤
        elif direction == "DOWN":
            pyautogui.scroll(-20)  # 아래로 스크롤

    def get_current_position(self):
        """현재 마우스 위치 반환"""
        return pyautogui.position()