from environment.simulator import VirtualComputerEnvironment
from ai_agent.agent import ComputerInteractionAgent
from command_processor.processor import CommandProcessor
from vision.vision_system import SimulatedVisionSystem


def main():
    environment = VirtualComputerEnvironment()
    command_processor = CommandProcessor(environment)
    vision_system = SimulatedVisionSystem(environment)

    agent = ComputerInteractionAgent()

    for _ in range(10):
        action = agent.choose_action()

        command_processor.process_command(action)

        vision_system.interpret_environment()

    print("Simulation complete.")


if __name__ == "__main__":
    main()
