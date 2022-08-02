# since we encounter this [problem](https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/distribute/multi_worker_with_keras.ipynb?hl=id-IDCache#scrollTo=Mhq3fzyR5hTw)
# it must put on the file starts before initialize other class and after set env.
from trainers import get_trainer
from utils.args_parser import solve_args
args = solve_args(multi_worker_strategy=True)

import os, time, json

import numpy as np
import tensorflow as tf
from datasets import get_dataset
from trainers import get_trainer

def save_log(history, val_metric: str=None):
    logs = {
        'config': vars(args),
        'history': history,
    }

    if val_metric != None:
        logs['best_acc'] = max(history[val_metric])
        print('Best score: ', logs['best_acc'])

    dir_path = os.path.dirname(os.path.realpath(__file__))
    logfile_name = dir_path + f'/logs/{args.model}-{int(time.time())}.json'
    os.makedirs(os.path.dirname(logfile_name), exist_ok=True)
    with open(logfile_name, 'w') as f:
        json.dump(logs, f, indent=4)
    print('Log file saved at: ', logfile_name)

def main(args):
    # Set random seeds
    np.random.seed(42)
    tf.random.set_seed(42)

    print("Version: ", tf.__version__)
    print("Eager mode: ", tf.executing_eagerly())
    print("GPU is", "available" if tf.config.list_physical_devices("GPU") else "NOT AVAILABLE")

    dataset = get_dataset(args.dataset)
    trainer = get_trainer(dataset.getTask())
    fitting = trainer.train(args, dataset)

    if dataset.getTask() == 'classification':
        if dataset.getOutputSize() > 2:
            save_log(fitting.history, 'val_categorical_accuracy')
        else:
            save_log(fitting.history, 'val_binary_accuracy')
    if dataset.getTask() == 'mlm':
        save_log(fitting.history)

if __name__ == '__main__':
    main(args)
