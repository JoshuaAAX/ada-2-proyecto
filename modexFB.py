from typing import List, Tuple
import math
import itertools


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
    
    
def calculate_effort(rs: SocialNetwork, strategy) -> int:
    total_effort = 0
    
    for i, mod in enumerate(strategy):
        if mod == 1:
            agent = rs.agents[i]
            effort = math.ceil(abs(agent.opinion) * (1 - agent.receptivity))
            total_effort += effort
            
    return total_effort
    


agent1 = Agent(opinion=-30, receptivity=0.9)
agent2 = Agent(opinion=40, receptivity=0.1)
agent3 = Agent(opinion=50, receptivity=0.5)
network = SocialNetwork(agents=[agent1, agent2, agent3], r_max=35)
"""
network_mod = apply_strategy(network, [0,0,1])
print(f"la nueva estrategia es: {network_mod}")

esfuerzo = calculate_effort(network, [0,0,1])
print(f"El nivel de esfuerzo  es: {esfuerzo}")

extremismo = calculate_extremism(network_mod)
print(f"El nivel de extremismo de la red social es: {extremismo:.4f}")
"""


def modexFB(rs: SocialNetwork):
    n = len(rs.agents)
    best_strategy = None
    best_extremism = float('inf')
    best_effort = 0
    
    for strategy in itertools.product([0,1], repeat=n):
        effort = calculate_effort(rs, strategy)
        
        if effort > rs.r_max:
            continue
            
        new_mod= apply_strategy(rs, strategy)
        extremism = calculate_extremism(new_mod)
            
        if extremism < best_extremism or (extremism == best_extremism and effort < best_effort):
            best_strategy = strategy
            best_extremism = extremism
            best_effort = effort
    
    return best_strategy, best_effort, best_extremism
        
        
#print(modexFB(network))