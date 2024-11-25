def merge_intervals(intervals_list):
    if not intervals_list:
        return []

    pairs = [
        (intervals_list[_], intervals_list[_ + 1])
        for _ in range(0, len(intervals_list), 2)
    ]
    pairs.sort(key=lambda x: x[0])

    merged = []
    current_start, current_end = pairs[0]

    for start_, end_ in pairs[1:]:
        if start_ <= current_end:
            current_end = max(current_end, end_)
        else:
            merged.extend([current_start, current_end])
            current_start, current_end = start_, end_

    merged.extend([current_start, current_end])
    return merged


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals["lesson"]

    pupil_intervals = merge_intervals(intervals["pupil"])
    tutor_intervals = merge_intervals(intervals["tutor"])

    timeline = []

    for _ in range(0, len(pupil_intervals), 2):
        start = max(pupil_intervals[_], lesson_start)
        end = min(pupil_intervals[_ + 1], lesson_end)
        if start < end:
            timeline.append((start, "pupil", True))
            timeline.append((end, "pupil", False))

    for _ in range(0, len(tutor_intervals), 2):
        start = max(tutor_intervals[_], lesson_start)
        end = min(tutor_intervals[_ + 1], lesson_end)
        if start < end:
            timeline.append((start, "tutor", True))
            timeline.append((end, "tutor", False))

    timeline.sort()

    total_time = 0
    last_timestamp = None
    pupil_present = False
    tutor_present = False

    for timestamp, person, is_entry in timeline:
        if pupil_present and tutor_present and last_timestamp is not None:
            if timestamp <= lesson_end and last_timestamp >= lesson_start:
                total_time += timestamp - last_timestamp

        if person == "pupil":
            pupil_present = is_entry
        else:
            tutor_present = is_entry

        last_timestamp = timestamp

    return total_time


if __name__ == "__main__":
    print(
        appearance(
            {
                "lesson": [1594663200, 1594666800],
                "pupil": [
                    1594663340,
                    1594663389,
                    1594663390,
                    1594663395,
                    1594663396,
                    1594666472,
                ],
                "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
            }
        )
    )
