import gym
from gym import spaces
from stable_baselines3 import PPO
import numpy as np
from settings import *

class KamiNoKenEnv(gym.Env):
    def __init__(self, game=None):
        super().__init__()
        self.game = game

        # Define action and observation spaces
        self.action_space = spaces.Discrete(10)  # Number of actions: move up, down, left, right, punch, kick, etc.

        # game image representation
        #self.observation_space = spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3), dtype=np.uint8)

        # game state representation
        self.get_observation_space()

    def step(self, action):
        # Update the game state based on the action taken
        self.game.frame_step()

        # Calculate the reward based on the game state
        reward = self.game.calculate_reward()

        # Check if the game is over
        done = self.game.over

        # Get the new observation (state representation)
        observation = self.get_observation_space()

        return observation, reward, done, {}

    def reset(self):
        # Reset the game state
        self.game.reset()

        # Get the initial observation
        initial_observation = self.get_observation_space()
        return initial_observation

    def get_observation_space(self):
        data = [
            self.game.player1_health,
            self.game.player2_health,
            self.game.player1_x,
            self.game.player1_y,
            self.game.player2_x,
            self.game.player2_y
        ]
        return spaces.Box(low=np.array(data), high=np.array([100, 100, width, height, width, height]), dtype=np.float32)

def load():
    return PPO.load("street_fighter_2_ppo")

    # In the game loop
    """
    observation = env.reset()
    done = False

    while not done:
        action, _ = trained_model.predict(observation, deterministic=True)
        observation, reward, done, info = env.step(action)
        env.render()
    """

def train():
    env = KamiNoKenEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=1_000_000)
    model.save("kami_no_ken_ppo")

# train AI
if __name__ == "__main__":
    train()