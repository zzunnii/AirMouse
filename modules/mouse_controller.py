import pyautogui
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class MouseController:
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.last_x = None
        self.last_y = None
        self.movement_scale = 0.08  # 마우스 움직임 배율 (조절 가능)

    def move_mouse(self, hand_landmark):
        """손의 움직임에 따라 마우스 상대적 이동"""
        current_x = hand_landmark.x
        current_y = hand_landmark.y

        if self.last_x is not None and self.last_y is not None:
            # 이전 위치와의 차이 계산
            delta_x = (current_x - self.last_x) * self.screen_width * self.movement_scale
            delta_y = (current_y - self.last_y) * self.screen_height * self.movement_scale

            # 현재 마우스 위치
            mouse_x, mouse_y = pyautogui.position()

            # 새로운 위치 계산
            new_x = mouse_x + int(delta_x)
            new_y = mouse_y + int(delta_y)

            # 화면 범위 내로 제한
            new_x = max(0, min(new_x, self.screen_width))
            new_y = max(0, min(new_y, self.screen_height))

            # 마우스 이동
            pyautogui.moveTo(new_x, new_y, duration=0.1)
            return new_x, new_y

        self.last_x = current_x
        self.last_y = current_y
        return pyautogui.position()

    def click(self):
        """마우스 클릭"""
        pyautogui.click()

    def scroll(self, amount):
        """스크롤"""
        pyautogui.scroll(amount)

    def press_enter(self):
        """엔터 키 입력"""
        pyautogui.press('enter')