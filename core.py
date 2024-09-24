from typing import List
import math

class Agent:
    def __init__(self, opinion: int, receptivity: float):
        self.opinion = opinion
        self.receptivity = receptivity

class SocialNetwork:
    def __init__(self, agents: List[Agent], r_max: int):
        self.agents = agents
        self.r_max = r_max
        
        
def calculate_extremism(rs: SocialNetwork) -> float:
    opinions = [agent.opinion**2 for agent in rs.agents]
    return math.sqrt(sum(opinions)) / len(rs.agents)

def apply_strategy(rs: SocialNetwork, strategy) -> SocialNetwork:
    agents = [ 
        Agent(0 if moderation else agent.opinion, agent.receptivity) 
        for agent, moderation in zip(rs.agents, strategy)
    ]
    
    return SocialNetwork(agents, rs.r_max)