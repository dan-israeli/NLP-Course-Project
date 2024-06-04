import wandb
YOUR_WANDB_USERNAME = "Please enter your organization name"
project = "Please enter your organization name"

command = [
        "${ENVIRONMENT_VARIABLE}",
        "${interpreter}",
        "StrategyTransfer.py",
        "${project}",
        "${args}"
    ]

sweep_config = {
    "name": "Best New Language-Based Strategy (Positive Only) Comprehensive Performance",
    "method": "grid",
    "metric": {
        "goal": "maximize",
        "name": "AUC.test.max"
    },
    "parameters": {
        "ENV_HPT_mode": {"values": [False]},
	    "architecture": {"values": ["LSTM", "transformer"]},
        "features": {"values": ["EFs"]},
        "online_simulation_factor": {"values": [0, 0.5, 1, 2, 4, 10]},
        "simulation_user_improve": {"values": [0.01]},
        "basic_nature": {"values": [17]},
	    "total_epochs": {"values": [25]},
        "seed": {"values": list(range(1, 4))}
    },
    "command": command
}

# Initialize a new sweep (original)
sweep_id = wandb.sweep(sweep=sweep_config, project=project)
print("run this line to run your agent in a screen:")
print(f"screen -dmS \"sweep_agent\" wandb agent {YOUR_WANDB_USERNAME}/{project}/{sweep_id}")
