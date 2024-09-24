from typing import List, Tuple
import math

class Agent:
    def __init__(self, opinion: int, receptivity: float):
        self.opinion = opinion
        self.receptivity = receptivity

class SocialNetwork:
    def __init__(self, agents: List[Agent], r_max: int):
        self.agents = agents
        self.r_max = r_max

def calculate_extremism(opinions: List[int]) -> float:
    return math.sqrt(sum(opinion**2 for opinion in opinions)) / len(opinions)

def calculate_effort(agent: Agent, moderate: bool) -> int:
    return math.ceil(abs(agent.opinion) * (1 - agent.receptivity)) if moderate else 0

def modexPD(rs: SocialNetwork) -> Tuple[List[int], int, float]:
    n = len(rs.agents)
    dp = [[[float('inf'), None] for _ in range(rs.r_max + 1)] for _ in range(n + 1)]
    
    # Base case: no agents, zero effort
    for effort in range(rs.r_max + 1):
        dp[0][effort] = [0, []]

    for i in range(1, n + 1):
        agent = rs.agents[i - 1]
        for effort in range(rs.r_max + 1):
            # Don't moderate this agent
            not_moderate = dp[i-1][effort][0] + agent.opinion**2
            dp[i][effort] = [not_moderate, dp[i-1][effort][1] + [0]]

            # Try to moderate if we have enough effort
            mod_effort = calculate_effort(agent, True)
            if effort >= mod_effort:
                moderate = dp[i-1][effort - mod_effort][0]
                if moderate < dp[i][effort][0]:
                    dp[i][effort] = [moderate, dp[i-1][effort - mod_effort][1] + [1]]

    # Find the best solution
    best_effort = min(range(rs.r_max + 1), key=lambda e: dp[n][e][0])
    best_strategy = dp[n][best_effort][1]
    best_extremism = math.sqrt(dp[n][best_effort][0]) / n

    return best_strategy, best_effort, best_extremism

# Example usage:
agent1 = Agent(opinion=-30, receptivity=0.9)
agent2 = Agent(opinion=40, receptivity=0.1)
agent3 = Agent(opinion=50, receptivity=0.5)
network = SocialNetwork(agents=[agent1, agent2, agent3], r_max=35)

best_strategy, best_effort, best_extremism = modex_dp(network)
print(f"Best strategy: {best_strategy}")
print(f"Best effort: {best_effort}")
print(f"Best extremism: {best_extremism:.4f}")