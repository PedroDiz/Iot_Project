from processor.processors.activityTimeProcessor import ActivityTimeProcessor
from processor.processors.caloriesProcessor import CaloriesProcessor
from processor.repository import MovementDatabase
from processor.processors.stepProcessor import StepProcessor

repo = MovementDatabase("127.0.0.1", "db", "dbuser", "changeit")

def main():
    movements = repo.retrieve_movement(64852)

    #print movements length
    print(len(movements))

    person_data = repo.retrieve_person(64852)
    step_processor = StepProcessor()
    steps, distance_covered = step_processor.process(person_data, movements)
    step_processor.send_data_to_nodered(steps, distance_covered)

    calories_processor = CaloriesProcessor()
    calories_burned = calories_processor.process(person_data, movements)
    calories_processor.send_data_to_nodered(calories_burned)

    activity_time_processor = ActivityTimeProcessor()
    activity_time = activity_time_processor.process(movements)
    activity_time_processor.send_data_to_nodered(activity_time)



if __name__ == "__main__":
    main()