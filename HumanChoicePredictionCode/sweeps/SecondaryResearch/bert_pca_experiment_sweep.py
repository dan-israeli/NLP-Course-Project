import wandb
YOUR_WANDB_USERNAME = "nlp_project87"
project = "Please enter the project name"

command = [
        "${ENVIRONMENT_VARIABLE}",
        "${interpreter}",
        "StrategyTransfer.py",
        "${project}",
        "${args}"
    ]

sweep_config = {
    "name": "BERT PCA Experiment",
    "method": "grid",
    "metric": {
        "goal": "maximize",
        "name": "AUC.test.max"
    },
    "parameters": {
        "ENV_HPT_mode": {"values": [False]},
        "architecture": {"values": ["LSTM"]},
        "features": {"values": [f"BERT_PCA_{i}" for i in range(5, 255, 5)]},
        "online_simulation_factor": {"values": [4]},
        "simulation_user_improve": {"values": [0.01]},
        "basic_nature": {"values": [12]},
        "total_epochs": {"values": [20]},
        "seed": {"values": list(range(1, 4))}
    },
    "command": command
}

# Initialize a new sweep
sweep_id = wandb.sweep(sweep=sweep_config, project=project)
print("run this line to run your agent in a screen:")
print(f"screen -dmS \"sweep_agent\" wandb agent {YOUR_WANDB_USERNAME}/{project}/{sweep_id}")
