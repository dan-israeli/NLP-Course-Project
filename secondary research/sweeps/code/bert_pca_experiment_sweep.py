import wandb
YOUR_WANDB_USERNAME = "nlp_project87"
project = "NLP_Project"

command = [
        "${ENVIRONMENT_VARIABLE}",
        "${interpreter}",
        "StrategyTransfer.py",
        "${project}",
        "${args}"
    ]

sweep_config = {
    "name": "BERT PCA Experiment - Completion 2",
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

print("Run these lines to run your agent in a screen:")
parallel_num = 6

if parallel_num > 10:
    print('Are you sure you want to run more than 10 agents in parallel? It would result in a CPU bottleneck.')
for i in range(parallel_num):
    print(f"screen -dmS \"final_sweep_agent_{i}\" nohup wandb agent {YOUR_WANDB_USERNAME}/{project}/{sweep_id}")
