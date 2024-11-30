class CaloriesProcessor:

    velocity_map = {
        range(20, 30): {"male": 1.36, "female": 1.34},
        range(30, 40): {"male": 1.43, "female": 1.34},
        range(40, 50): {"male": 1.45, "female": 1.39},
        range(50, 60): {"male": 1.43, "female": 1.31},
        range(60, 70): {"male": 1.34, "female": 1.24},
        range(70, 80): {"male": 1.26, "female": 1.13},
        range(80, 90): {"male": 0.97, "female": 0.94},
    }

    def process(self, person_data, movement_data):

        # Retrieve age, weight, height, gender from person_data
        age = person_data[1]
        weight = person_data[2]
        height = person_data[3]
        gender = "male" # for now, because db doesn't have this attribute

        # Retrieve activity from movement_data
        activity_values = [item[2] for item in movement_data]

        # Calculate burnt calories
        for age_range, genders in self.velocity_map.items():
            if age in age_range:
                velocity = genders.get(gender)
                break

        # Split the activity array into blocks of 60 and apply the formula
        # Depending on the activity, the velocity is multiplied by 2
        # An average is taken of the activity values in the block

        burnt_calories = 0
        for i in range(0, len(activity_values), 60):
            activity = sum(activity_values[i:i+60]) / 60
            # If the activity average is above 0.5 multiply the velocity by 2
            if activity > 0.5:
                velocity *= 2

            burnt_calories += 0.035 * weight + ((velocity ** 2) / height) * 0.029 * weight
        return burnt_calories
