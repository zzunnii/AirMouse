import pyautogui
import time
from config.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SKELETON_WIDTH,
    SKELETON_HEIGHT,
    BOX_PADDING,
    HOVER_CLICK_DELAY,
    POSITION_LOCK_TIME,
    MOVEMENT_THRESHOLD
)

class MouseController:
   def __init__(self):
       pyautogui.FAILSAFE = False

       # 바운딩 박스 정보 계산
       self.box_width = SKELETON_WIDTH + (BOX_PADDING * 2)
       self.box_height = SKELETON_HEIGHT + (BOX_PADDING * 2)

       self.screen_width = SCREEN_WIDTH
       self.screen_height = SCREEN_HEIGHT

       self.last_x = None
       self.last_y = None
       self.is_dragging = False

       # 위치 고정 관련 변수
       self.position_lock_time = None
       self.locked_position = None
       self.is_position_locked = False

       # 자동 클릭 관련 변수
       self.hover_start_time = None
       self.last_click_time = 0
       self.hover_position = None

   def check_clickable_element(self):
       """현재 마우스 위치의 UI 요소가 클릭 가능한지 확인"""
       try:
           # 여기서 운영체제별 UI 요소 감지 로직 구현 필요
           # 임시로 True 반환
           return True
       except:
           return False

   def is_text_input_area(self):
       """현재 마우스 위치가 텍스트 입력 영역인지 확인"""
       try:
           # 여기서 운영체제별 텍스트 입력 영역 감지 로직 구현 필요
           # 임시로 False 반환
           return False
       except:
           return False

   def has_significant_movement(self, new_x, new_y):
       """의미있는 마우스 이동이 있었는지 확인"""
       if self.last_x is None or self.last_y is None:
           return True

       distance = ((new_x - self.last_x) ** 2 + (new_y - self.last_y) ** 2) ** 0.5
       return distance > MOVEMENT_THRESHOLD

   def move_mouse(self, hand_landmark):
       rel_x = hand_landmark.x
       rel_y = hand_landmark.y

       screen_x = rel_x * self.screen_width
       screen_y = rel_y * self.screen_height

       if self.last_x is not None:
           screen_x = self.last_x + (screen_x - self.last_x) * 0.5
           screen_y = self.last_y + (screen_y - self.last_y) * 0.5

       # 의미있는 움직임 체크
       if self.has_significant_movement(screen_x, screen_y):
           self.is_position_locked = False
           self.position_lock_time = None
           self.hover_start_time = None

       current_time = time.time()

       # 클릭 가능한 요소 위에서 위치 고정
       if self.check_clickable_element() and not self.is_position_locked:
           if self.position_lock_time is None:
               self.position_lock_time = current_time
               self.locked_position = (screen_x, screen_y)
           elif current_time - self.position_lock_time > POSITION_LOCK_TIME:
               self.is_position_locked = True
               screen_x, screen_y = self.locked_position

       # 텍스트 입력 영역에서 자동 클릭
       if self.is_text_input_area():
           if self.hover_start_time is None:
               self.hover_start_time = current_time
               self.hover_position = (screen_x, screen_y)
           elif current_time - self.hover_start_time > HOVER_CLICK_DELAY:
               if current_time - self.last_click_time > HOVER_CLICK_DELAY:
                   self.click(self.hover_position[0], self.hover_position[1])
                   self.last_click_time = current_time
                   self.hover_start_time = None

       screen_x = max(0, min(screen_x, self.screen_width))
       screen_y = max(0, min(screen_y, self.screen_height))

       self.last_x = screen_x
       self.last_y = screen_y

       if not self.is_position_locked:
           pyautogui.moveTo(screen_x, screen_y, duration=0.05)
       return screen_x, screen_y

   def click(self, x=None, y=None):
       """마우스 클릭"""
       if x is not None and y is not None:
           pyautogui.click(x=x, y=y)
       else:
           pyautogui.click()

   def double_click(self, x=None, y=None):
       """더블 클릭"""
       if x is not None and y is not None:
           pyautogui.doubleClick(x=x, y=y)
       else:
           pyautogui.doubleClick()

   def start_drag(self, x=None, y=None):
       """드래그 시작"""
       if x is not None and y is not None:
           pyautogui.mouseDown(x=x, y=y)
       else:
           pyautogui.mouseDown()
       self.is_dragging = True

   def end_drag(self, x=None, y=None):
       """드래그 종료"""
       if self.is_dragging:
           if x is not None and y is not None:
               pyautogui.mouseUp(x=x, y=y)
           else:
               pyautogui.mouseUp()
           self.is_dragging = False