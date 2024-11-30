# utils/math_utils.py
import math


def calculate_distance(p1, p2):
    """두 점 사이의 유클리드 거리 계산

    Args:
        p1: 첫 번째 점 (x, y 속성을 가진 객체)
        p2: 두 번째 점 (x, y 속성을 가진 객체)

    Returns:
        float: 두 점 사이의 거리
    """
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def calculate_angle(p1, p2, p3):
    """세 점으로 이루어진 각도 계산

    Args:
        p1: 첫 번째 점 (x, y 속성을 가진 객체)
        p2: 중심점 (x, y 속성을 가진 객체)
        p3: 세 번째 점 (x, y 속성을 가진 객체)

    Returns:
        float: 각도 (도 단위)
    """
    angle = math.degrees(
        math.atan2(p3.y - p2.y, p3.x - p2.x) -
        math.atan2(p1.y - p2.y, p1.x - p2.x)
    )

    if angle < 0:
        angle += 360
    return angle


def smooth_value(current, target, factor=0.3):
    """값을 부드럽게 보간

    Args:
        current: 현재 값
        target: 목표 값
        factor: 보간 계수 (0~1, 클수록 더 빠르게 목표값에 도달)

    Returns:
        float: 보간된 값
    """
    return current + (target - current) * factor


def normalize_coordinates(x, y, source_width, source_height, target_width, target_height):
    """좌표를 다른 해상도로 변환

    Args:
        x, y: 원본 좌표
        source_width, source_height: 원본 해상도
        target_width, target_height: 목표 해상도

    Returns:
        tuple: (변환된 x 좌표, 변환된 y 좌표)
    """
    normalized_x = (x / source_width) * target_width
    normalized_y = (y / source_height) * target_height
    return normalized_x, normalized_y