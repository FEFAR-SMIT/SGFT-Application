def get_angle_segment(angle, segment_size=5):
    """
    Get the segment number for a given angle (0-359 degrees / segment_size)
    """
    return int(angle // segment_size)
