import subprocess
import os

def launch_tensorboard():
    # Define the path to the TensorBoard script
    tensorboard_script = os.path.join('C:\\', 'Users', 'aarya', 'AppData', 'Local', 'Packages',
                                      'PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0', 'LocalCache',
                                      'local-packages', 'Python311', 'Scripts', 'tensorboard')

    # Command to start TensorBoard
    command = [tensorboard_script, '--logdir=path_to_your_logs', '--bind_all']

    # Run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print('TensorBoard started successfully')
    else:
        print('Failed to start TensorBoard')
        print('Error:', stderr.decode())

# Specify the path to your logs directory
logdir = "logs/dqn_intelligoal_tensorboard/DQN_4/events.out.tfevents.1712996877.Panigrahi.7612.2"

# Call the function with the path to the logs
launch_tensorboard()
