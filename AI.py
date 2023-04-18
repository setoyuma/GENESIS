import gym
from gym import spaces
from stable_baselines3 import PPO
import numpy as np

import main

class KamiNoKenEnv(gym.Env):
    def __init__(self, game=None):
        super().__init__()
        self.game = game
        self.player1_model = None
        self.player2_model = None

        # Define action and observation spaces
        self.action_space = spaces.Discrete(10)  # Number of actions: move up, down, left, right, punch, kick, etc.

        # game image representation
        #self.observation_space = spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3), dtype=np.uint8)

    def step(self, action):
        # Update the game state based on the action taken
        self.game.frame_step()

        # Calculate the reward based on the game state
        reward = self.game.calculate_reward()

        # Check if the game is over
        done = self.game.over

        # Get the new observation (state representation)
        observation = self.fighter_to_observation(self.game.player1.to_dict())
        return observation, reward, done, {}

    def reset(self):
        # Reset the game state
        self.game.reset()

        # Get the initial observation
        initial_observation = self.fighter_to_observation(self.game.player1.to_dict())
        return initial_observation

    def get_observation_space(self):
        fighter_data = self.fighter_to_observation(self.game.player1.to_dict())
        low = np.zeros_like(fighter_data)
        high = np.full_like(fighter_data, np.inf)  # You may want to adjust the high limits according to your game's constraints
        return spaces.Box(low=low, high=high, dtype=np.float32)

    def fighter_to_observation(self, fighter):
        data = [
            fighter['frame_index'],
            fighter['current_hp'],
            fighter['super_meter'],
            fighter['blast_meter'],
            fighter['speed'],
            fighter['status'],
            fighter['rect'][0],  # x
            fighter['rect'][1],  # y
            fighter['rect'][2],  # width
            fighter['rect'][3],  # height
            fighter['hit_box'][0],  # x
            fighter['hit_box'][1],  # y
            fighter['hit_box'][2],  # width
            fighter['hit_box'][3],  # height
            int(fighter['on_ground']),
            int(fighter['alive']),
            int(fighter['facing_right']),
            fighter['dX'],
            fighter['dY'],
            fighter['gravity'],
            fighter['jump_force'],
            fighter['move_speed']
        ]
        return np.array(data, dtype=np.float32)


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

def train_self_play():
    env = KamiNoKenEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    env.player1_model = model  # Set player1_model to use the PPO model
    env.player2_model = model  # Set player2_model to use the same PPO model for self-play

    model.learn(total_timesteps=1_000_000)
    model.save("kami_no_ken_ppo_self_play")

if __name__ == "__main__":
    game.reset()  # init player vars
    game.init_training_vars()
    AI.train()