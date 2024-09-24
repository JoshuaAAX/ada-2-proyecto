from typing import List, Tuple
import math

from core import *


def modexV(rs: SocialNetwork) -> Tuple[List[int], int, float]:
    n = len(rs.agents)
    strategy = [0] * n
    effort = 0
    
    sorted_agents = sorted(
        enumerate(rs.agents),
        key=lambda x: abs(x[1].opinion) / (1 - x[1].receptivity),
        reverse=True
    )
    
    for idx, agent in sorted_agents:
        agent_effort = math.ceil(abs(agent.opinion) * (1 - agent.receptivity))
        
        if effort + agent_effort <= rs.r_max:
            strategy[idx] = 1
            effort += agent_effort
        
        if effort == rs.r_max:
            break
    
    moderated_network = apply_strategy(rs, strategy)
    extremism = calculate_extremism(moderated_network)
    
    return strategy, effort, extremism