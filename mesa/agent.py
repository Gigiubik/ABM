"""
The agent class for Mesa framework.

Core Objects: Agent

"""
# mypy
from typing import Optional, TYPE_CHECKING
from random import Random

if TYPE_CHECKING:
    # We ensure that these are not imported during runtime to prevent cyclic
    # dependency.
    from mesa.model import Model
    from mesa.space import Position


class Agent:
    """Base class for a model agent."""

    def __init__(self, unique_id: int, model: "Model") -> None:
        """Create a new agent.

        Args:
            unique_id (int): A unique numeric identified for the agent
            model: (Model): Instance of the model that contains the agent
        """
        self.unique_id = unique_id
        self.model = model
        self.pos: Optional[Position] = None
        self.heading = 90

    def step(self) -> None:
        """A single step of the agent."""
        pass

    def advance(self) -> None:
        pass

    def move_forward_or_backward(self, amount, sign):
        """Does the calculation to find  the agent's next move and is used within the forward and backward functions"""
        new_x = float(self.pos[0]) + sign * math.cos(self.heading * math.pi / 180) * amount
        new_y = float(self.pos[1]) + sign * math.sin(self.heading * math.pi / -180) * amount
        next_pos = (new_x, new_y)
        try:
            self.model.space.move_agent(self, next_pos)
        except:
            print("agent.py (forward_backwards): could not move agent within self.model.space")

    def move_forward(self, amount):
        """Moves the agent forward by the amount given"""
        self.move_forward_or_backward(amount, 1)

    def move_backward(self, amount):
        """Moves the agent backwards from where its facing by the given amount"""
        self.move_forward_or_backward(amount, -1)

    def turn_right(self, degree):
        """Turns the agent right by the given degree"""
        self.heading = (self.heading - degree) % 360

    def turn_left(self, degree):
        """Turns the agent left by the given degree"""
        self.heading = (self.heading + degree) % 360

    def setxy(self, x, y):
        """Sets the current position to the specified x,y parameters"""
        self.pos = (x, y)

    def set_pos(self, apos):
        """Sets the current position to the specified pos parameter"""
        self.pos = apos

    def distancexy(self, x, y):
        """Gives you the distance of the agent and the given coordinate"""
        return math.dist(self.pos, (x, y))

    def distance(self, another_agent):
        """Gives you the distance between the agent and another agent"""
        return self.distancexy(another_agent.pos[0], another_agent.pos[1])

    def die(self):
        """Removes the agent from the schedule and the grid """
        try:
            self.model.schedule.remove(self)
        except:
            print("agent.py (die): could not remove agent from self.model.schedule")
        try:
            self.model.space.remove_agent(self)
        except:
            print("agent.py (die): could not remove agent from self.model.space")

    def towardsxy(self, x, y):
        """Calculates angle between a given coordinate and horizon as if the current position is the origin"""
        dx = x - float(self.pos[0])
        dy = float(self.pos[1]) - y
        if dx == 0:
            return 90 if dy > 0 else 270
        else:
            return math.degrees(math.atan2(dy, dx))

    def towards(self, another_agent):
        """Calculates angle between an agent and horizon as if the current position is the origin"""
        return self.towardsxy(*another_agent.pos)

    def facexy(self, x, y):
        """Makes agent face a given coordinate"""
        self.heading = self.towardsxy(x, y)

    def face(self, another_agent):
        """Makes agent face another agent"""
        x, y = another_agent.pos
        self.facexy(x, y)

    @property
    def random(self) -> Random:
        return self.model.random
