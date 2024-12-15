import pyautogui
from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SKELETON_WIDTH,
    SKELETON_HEIGHT,
    MOVEMENT_SMOOTHING, MOUSEPAD_MARGIN, MOUSE_SENSITIVITY
)


class MouseController:
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.last_x = None
        self.last_y = None

    def is_in_mousepad(self, x, y):
        """주어진 좌표가 마우스패드 영역 내에 있는지 확인"""
        pad_left = MOUSEPAD_MARGIN / SKELETON_WIDTH
        pad_right = (SKELETON_WIDTH - MOUSEPAD_MARGIN) / SKELETON_WIDTH
        pad_top = MOUSEPAD_MARGIN / SKELETON_HEIGHT
        pad_bottom = (SKELETON_HEIGHT - MOUSEPAD_MARGIN) / SKELETON_HEIGHT

        return (pad_left <= x <= pad_right and
                pad_top <= y <= pad_bottom)

    def move_mouse(self, hand_landmark):
        """스켈레톤 전체 영역에서의 마우스 이동"""
        current_x, current_y = pyautogui.position()

        # 현재 손의 좌표
        x = hand_landmark.x
        y = hand_landmark.y

        if self.last_x is not None and self.last_y is not None:
            # 움직임 변화량 계산
            delta_x = (x - self.last_x)
            delta_y = (y - self.last_y)

            # 미세한 움직임 무시 (노이즈 제거)
            if abs(delta_x) < 0.001 and abs(delta_y) < 0.001:
                return current_x, current_y


            # 실제 화면 크기에 맞게 스케일링
            scaled_delta_x = delta_x * SCREEN_WIDTH * MOUSE_SENSITIVITY
            scaled_delta_y = delta_y * SCREEN_HEIGHT * MOUSE_SENSITIVITY

            # 움직임 부드럽게 (더 낮은 값으로 조정)
            smoothed_delta_x = scaled_delta_x * 0.3  # MOVEMENT_SMOOTHING 값도 낮춤
            smoothed_delta_y = scaled_delta_y * 0.3

            # 새로운 마우스 위치 계산
            new_x = current_x + int(smoothed_delta_x)
            new_y = current_y + int(smoothed_delta_y)

            # 화면 범위 제한
            new_x = max(0, min(new_x, self.screen_width))
            new_y = max(0, min(new_y, self.screen_height))

            # 마우스 이동
            pyautogui.moveTo(new_x, new_y)

        # 현재 위치를 이전 위치로 저장
        self.last_x = x
        self.last_y = y

        return current_x, current_y

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