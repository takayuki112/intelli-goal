import gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

# Create the CartPole environment
# env_name = "CartPole-v1"
env = gym.make('CartPole-v1', render_mode='human')


# Wrap it for use with Stable Baselines3
env = DummyVecEnv([lambda: env])

# Initialize the agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
model.learn(total_timesteps=20000)

# Evaluate the trained agent
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
print(f"Mean reward: {mean_reward} +/- {std_reward}")

# Saving the model
model.save("ppo_cartpole")

# Load the model
model = PPO.load("ppo_cartpole")

# Enjoy trained agent
obs = env.reset()
for i in range(20000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()
env.close()
