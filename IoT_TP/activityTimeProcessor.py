class ActivityTimeProcessor():

    def convert_to_hours_minutes_seconds(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return hours, minutes, remaining_seconds

    def process(self, data):
        activity = [item[2] for item in data]

        # Calculate the time spent where activity = 0 and where activity = 1 given the date and time

        activities = {
            "walking": 0,
            "running": 0
        }

        for i in range(len(activity)):
            if activity[i] == 0:
                activities["walking"] += 1
            else:
                activities["running"] += 1

        # Convert this into hours, minutes, seconds

        walking_hours, walking_minutes, walking_seconds = self.convert_to_hours_minutes_seconds(activities["walking"])
        running_hours, running_minutes, running_seconds = self.convert_to_hours_minutes_seconds(activities["running"])

        activity_time = {
            "walking": {
                "hours": walking_hours,
                "minutes": walking_minutes,
                "seconds": walking_seconds
            },
            "running": {
                "hours": running_hours,
                "minutes": running_minutes,
                "seconds": running_seconds
            }
        }


        return activity_time

