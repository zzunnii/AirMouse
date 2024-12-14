import cv2
import numpy as np
from modules.hand_tracker import HandTracker
from modules.gesture_recognizer import GestureRecognizer
from modules.mouse_controller import MouseController
from config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    SKELETON_WIDTH, SKELETON_HEIGHT,
    BOX_PADDING, BOX_COLOR, BOX_THICKNESS,
    SKELETON_COLOR, DEBUG_MODE
)


def main():
    # 초기화
    hand_tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    mouse_controller = MouseController()

    # 스켈레톤 창 설정
    cv2.namedWindow('Hand Skeleton', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Hand Skeleton', SKELETON_WIDTH, SKELETON_HEIGHT)

    try:
        while True:
            # 웹캠 프레임 획득
            webcam_frame = hand_tracker.get_frame()
            if webcam_frame is None:
                continue

            # 스켈레톤 표시용 캔버스
            skeleton_display = np.zeros((SKELETON_HEIGHT, SKELETON_WIDTH, 3), dtype=np.uint8)

            # 바운딩 박스 그리기
            cv2.rectangle(skeleton_display,
                          (BOX_PADDING, BOX_PADDING),
                          (SKELETON_WIDTH - BOX_PADDING, SKELETON_HEIGHT - BOX_PADDING),
                          BOX_COLOR, BOX_THICKNESS)

            # 핸드 트래킹 수행
            results = hand_tracker.process_frame(webcam_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 검지 손가락 포즈 확인
                    if gesture_recognizer.check_index_finger_up(hand_landmarks):
                        # 마우스 이동 (항상 수행)
                        mouse_controller.move_mouse(hand_landmarks.landmark[8])

                        # 제스처 감지 및 처리
                        gesture, position = gesture_recognizer.update_gesture_state(hand_landmarks)

                        if gesture:
                            if DEBUG_MODE:
                                print(f"Gesture detected: {gesture}")

                            screen_x = position[0] * SCREEN_WIDTH
                            screen_y = position[1] * SCREEN_HEIGHT

                            if gesture == "SELECT":
                                if DEBUG_MODE:
                                    print("Executing SELECT")
                                mouse_controller.select(screen_x, screen_y)
                            elif gesture == "CLICK":
                                if DEBUG_MODE:
                                    print("Executing CLICK")
                                mouse_controller.click(screen_x, screen_y)
                            elif gesture == "DRAG":
                                if DEBUG_MODE:
                                    print("Executing DRAG")
                                mouse_controller.start_drag(screen_x, screen_y)
                            elif gesture == "DROP":
                                if DEBUG_MODE:
                                    print("Executing DROP")
                                mouse_controller.end_drag(screen_x, screen_y)

                    # 스켈레톤 그리기
                    hand_tracker.draw_landmarks(skeleton_display, hand_landmarks)

                    # 현재 상태 표시
                    if DEBUG_MODE:
                        mouse_pos = mouse_controller.get_current_position()
                        debug_info = f"Mouse: ({mouse_pos[0]}, {mouse_pos[1]})"
                        cv2.putText(skeleton_display, debug_info,
                                    (10, SKELETON_HEIGHT - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.4, SKELETON_COLOR, 1)

                        # 제스처 상태 표시
                        gesture_state = gesture if gesture else "POINTING" if gesture_recognizer.check_index_finger_up(
                            hand_landmarks) else "NONE"
                        cv2.putText(skeleton_display, f"Gesture: {gesture_state}",
                                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, SKELETON_COLOR, 1)

            # 스켈레톤 창 업데이트
            cv2.imshow('Hand Skeleton', skeleton_display)

            # ESC 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        # 리소스 정리
        hand_tracker.cleanup()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()