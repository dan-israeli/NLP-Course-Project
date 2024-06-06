import wandb
YOUR_WANDB_USERNAME = "Please_enter_your_organization_name"
project = "Please_enter_the_project_name"

command = [
        "${ENVIRONMENT_VARIABLE}",
        "${interpreter}",
        "StrategyTransfer.py",
        "${project}",
        "${args}"
    ]

sweep_config = {
    "name": "New Language-Based Strategies Experiment",
    "method": "grid",
    "metric": {
        "goal": "maximize",
        "name": "AUC.test.max"
    },
    "parameters": {
        "ENV_HPT_mode": {"values": [True]},
        "architecture": {"values": ["LSTM"]},
        "features": {"values": ["EFs"]},
        "online_simulation_factor": {"values": [2]},
        "simulation_user_improve": {"values": [0.005, 0.01, 0.02]},
        "basic_nature": {"values": list(range(17, 24))},
	"total_epochs": {"values": [20]},
        "seed": {"values": list(range(1, 4))}
    },
    "command": command
}

# Initialize a new sweep
sweep_id = wandb.sweep(sweep=sweep_config, project=project)
print("run this line to run your agent in a screen:")
print(f"screen -dmS \"sweep_agent\" wandb agent {YOUR_WANDB_USERNAME}/{project}/{sweep_id}")
