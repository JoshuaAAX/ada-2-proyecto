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

def calculate_effort(rs: SocialNetwork, strategy) -> int:
    total_effort = 0
    
    for i, mod in enumerate(strategy):
        if mod == 1:
            agent = rs.agents[i]
            effort = math.ceil(abs(agent.opinion) * (1 - agent.receptivity))
            total_effort += effort
            
    return total_effort

def apply_strategy(rs: SocialNetwork, strategy) -> SocialNetwork:
    agents = [ 
        Agent(0 if moderation else agent.opinion, agent.receptivity) 
        for agent, moderation in zip(rs.agents, strategy)
    ]
    
    return SocialNetwork(agents, rs.r_max)