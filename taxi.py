"""
Dans ce TP, nous allons implémenter un agent qui apprend à jouer au jeu Taxi-v3
de OpenAI Gym. Le but du jeu est de déposer un passager à une destination
spécifique en un minimum de temps. Le jeu est composé d'une grille de 5x5 cases
et le taxi peut se déplacer dans les 4 directions (haut, bas, gauche, droite).
Le taxi peut prendre un passager sur une case spécifique et le déposer à une
destination spécifique. Le jeu est terminé lorsque le passager est déposé à la
destination. Le jeu est aussi terminé si le taxi prend plus de 200 actions.

Vous devez implémenter un agent qui apprend à jouer à ce jeu en utilisant
les algorithmes Q-Learning et SARSA.

Pour chaque algorithme, vous devez réaliser une vidéo pour montrer que votre modèle fonctionne.
Vous devez aussi comparer l'efficacité des deux algorithmes en termes de temps
d'apprentissage et de performance.

A la fin, vous devez rendre un rapport qui explique vos choix d'implémentation
et vos résultats (max 1 page).
"""

import typing as t
import gymnasium as gym
from gymnasium.wrappers import RecordEpisodeStatistics, RecordVideo
import numpy as np
from qlearning import QLearningAgent
from qlearning_eps_scheduling import QLearningAgentEpsScheduling
from sarsa import SarsaAgent


env = gym.make("Taxi-v3", render_mode="rgb_array")
n_actions = env.action_space.n  # type: ignore


def evaluate_agent(agent, env, num_eval_episodes, video_folder):
    env = RecordVideo(env, video_folder=video_folder, name_prefix="eval", episode_trigger=lambda x: True)
    env = RecordEpisodeStatistics(env, deque_size=num_eval_episodes)

    for episode_num in range(num_eval_episodes):
        obs, info = env.reset()
        episode_over = False

        while not episode_over:
            action = agent.get_action(obs)  # Remplacez avec votre agent réel
            obs, reward, terminated, truncated, info = env.step(action)
            episode_over = terminated or truncated

    env.close()





#################################################
# 1. Play with QLearningAgent
#################################################

agent = QLearningAgent(
    learning_rate=0.05, epsilon=0.02, gamma=0.99, legal_actions=list(range(n_actions))
)


def play_and_train(env: gym.Env, agent: QLearningAgent, t_max=int(1e4)) -> float:
    """
    This function should
    - run a full game, actions given by agent.getAction(s)
    - train agent using agent.update(...) whenever possible
    - return total rewardb
    """
    total_reward: t.SupportsFloat = 0.0
    s, _ = env.reset()

    for _ in range(t_max):
        # Get agent to pick action given state s
        a = agent.get_action(s)

        next_s, r, done, _, _ = env.step(a)

        # Train agent for state s
        # BEGIN SOLUTION
        agent.update(s, a, r, next_s)

        total_reward += r
        s = next_s

        if done:
            break

        # env.render()
        # END SOLUTION

    return total_reward





rewards = []
for i in range(10000):
    rewards.append(play_and_train(env, agent))
    if i % 100 == 0:
        print("mean reward", np.mean(rewards[-100:]))

# assert np.mean(rewards[-100:]) > 0.0

# evaluate_agent(agent, env, num_eval_episodes=4, video_folder="video_qlearning")



# TODO: créer des vidéos de l'agent en action

#################################################
# 2. Play with QLearningAgentEpsScheduling
#################################################


agent = QLearningAgentEpsScheduling(
    learning_rate=0.05, epsilon=0.02, gamma=0.99, legal_actions=list(range(n_actions))
)

rewards = []
for i in range(10000):
    rewards.append(play_and_train(env, agent))
    if i % 100 == 0:
        print("mean reward", np.mean(rewards[-100:]))

# assert np.mean(rewards[-100:]) > 0.0
# TODO: créer des vidéos de l'agent en action

# evaluate_agent(agent, env, num_eval_episodes=4, video_folder="video_qlearningepssched")

####################
# 3. Play with SARSA
####################



def play_and_train_sarsa(env: gym.Env, agent: QLearningAgent, t_max=int(1e4)) -> float:
    """
    This function should
    - run a full game, actions given by agent.getAction(s)
    - train agent using agent.update(...) whenever possible
    - return total rewardb
    """
    total_reward: t.SupportsFloat = 0.0
    s, _ = env.reset()

    for _ in range(t_max):
        # Get agent to pick action given state s
        a = agent.get_action(s)

        next_s, r, done, _, _ = env.step(a)

        next_a = agent.get_action(next_s)
        # Train agent for state s
        # BEGIN SOLUTION
        agent.update(s, a, r, next_s, next_a)

        total_reward += r
        s = next_s
        if done:
            break

        # env.render()
        # END SOLUTION

    return total_reward



agent = SarsaAgent(learning_rate=0.05, epsilon=0.02, gamma=0.99, legal_actions=list(range(n_actions)))

rewards = []
for i in range(10000):
    rewards.append(play_and_train_sarsa(env, agent))
    if i % 100 == 0:
        print("mean reward", np.mean(rewards[-100:]))

# evaluate_agent(agent, env, num_eval_episodes=4, video_folder="video_sarsa")