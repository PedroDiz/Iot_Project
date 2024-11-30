from activityTimeProcessor import ActivityTimeProcessor
from repository import MovementDatabase
from stepProcessor import StepProcessor

repo = MovementDatabase("127.0.0.1", "db", "dbuser", "changeit")

def main():
    movements = repo.retrieve_movement(64852)
    step_processor = StepProcessor()
    steps = step_processor.process(movements)
    print(f"Number of steps: {steps}")


if __name__ == "__main__":
    main()