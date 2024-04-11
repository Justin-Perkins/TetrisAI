
from dqn_agent import DQNAgent
from tetris import Tetris
from tqdm import tqdm
        
def dqn():
    env = Tetris()
    episodes = 2000
    max_steps = None
    epsilon = 0
    epsilon_stop_episode = 1500
    mem_size = 20000
    discount = 0.95
    batch_size = 512
    epochs = 1
    render_every = 50
    log_every = 50
    replay_start_size = 2000
    train_every = 1
    n_neurons = [32, 32]
    render_delay = None
    activations = ['relu', 'relu', 'linear']

    agent = DQNAgent(env.get_state_size(),
                     n_neurons=n_neurons, activations=activations, epsilon=epsilon,
                     epsilon_stop_episode=epsilon_stop_episode, mem_size=mem_size,
                     discount=discount, replay_start_size=replay_start_size)
    
    agent.load('my_model.keras')
    

    scores = []

    for episode in tqdm(range(episodes)):
        current_state = env.reset()
        done = False
        steps = 0

        render = True

        print(agent.next_action(current_state))

        # Game
        while not done and (not max_steps or steps < max_steps):
            next_states = env.get_next_states()
            best_state = agent.best_state(next_states.values())
            
            best_action = None
            for action, state in next_states.items():
                if state == best_state:
                    best_action = action
                    break

            best_action = agent.next_action(current_state)

            reward, done = env.play(best_action[0], best_action[1], render=render,
                                    render_delay=render_delay)
            
            agent.add_to_memory(current_state, next_states[best_action], reward, done)
            current_state = next_states[best_action]
            steps += 1

        scores.append(env.get_game_score())

        # Train
        #if episode % train_every == 0:
        #    agent.train(batch_size=batch_size, epochs=epochs)

        # Logs
        #if log_every and episode and episode % log_every == 0:
            #avg_score = mean(scores[-log_every:])
            #min_score = min(scores[-log_every:])
            #max_score = max(scores[-log_every:])

            #log.log(episode, avg_score=avg_score, min_score=min_score,
            #        max_score=max_score)
    #agent.save("my_model.keras")


if __name__ == "__main__":
    dqn()
    