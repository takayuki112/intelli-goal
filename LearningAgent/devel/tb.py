import tensorboard
import subprocess
import webbrowser
from tensorboard import program

def launch_tensorboard(log_dir='logs/'):
    # Set up a TensorBoard instance
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', log_dir])

    # Start TensorBoard
    url = tb.launch()
    print(f"TensorBoard started at {url}")

    # Optionally, open a browser window to the TensorBoard URL
    webbrowser.open(url)

# Specify the directory where your TensorFlow logs are saved
log_directory = '.\logs\dqn_intelligoal_tensorboard\DQN_5\events.out.tfevents.1713007970.Panigrahi.9444.0'
log_directory = '.\logs\dqn_intelligoal_tensorboard\DQN_4\events.out.tfevents.1713007852.Panigrahi.6872.0'
launch_tensorboard(log_directory)
