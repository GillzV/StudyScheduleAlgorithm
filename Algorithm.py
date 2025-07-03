from collections import defaultdict

def generate_schedule(topics, days, daily_hours):
    """
    Study Schedule Generator
        topics: List of dicts with keys:
            - 'name': topic name
            - 'difficulty': Write an integer from 1 (easy) to 5 (hard)
            - 'estimated_time': hours per review session
        days: Number of days before deadline
        daily_hours: Max hours available per day
    Returns:
        Dictionary: {day_number: [(topic_name, time)]}
    """
    schedule = defaultdict(list)
    day_loads = [0] * (days + 1)  # 1-indexed

    # Sort harder topics first
    topics_sorted = sorted(topics, key=lambda x: -x['difficulty'])

    for topic in topics_sorted:
        name = topic['name']
        difficulty = topic['difficulty'] / 5.0  # Normalize to 0–1
        time_per_session = topic['estimated_time']


        # Compute review frequency (2 to 5 sessions)
        review_count = round(2 + 3 * difficulty)
        review_days = sorted(set(round(1 + (days - 1) * j / (review_count - 1)) for j in range(review_count)))


        for day in review_days:
            if day_loads[day] + time_per_session <= daily_hours:
                schedule[day].append((name, time_per_session))
                day_loads[day] += time_per_session
            else:
                # Try another day
                for alt_day in range(1, days + 1):
                    if day_loads[alt_day] + time_per_session <= daily_hours:
                        schedule[alt_day].append((name, time_per_session))
                        day_loads[alt_day] += time_per_session
                        break
    return dict(schedule)

# Sample Input

topics = [
    {"name": "Math", "difficulty": 5, "estimated_time": 1.5},
    {"name": "Biology", "difficulty": 3, "estimated_time": 1.0},
    {"name": "History", "difficulty": 1, "estimated_time": 0.5},
    {"name": "Chemistry", "difficulty": 4, "estimated_time": 1.2},
]

schedule = generate_schedule(topics, days=5, daily_hours=3)


for day in sorted(schedule):
    print(f"\nDay {day}:")
    for topic, hrs in schedule[day]:
        print(f"  - {topic}: {hrs} hrs")




