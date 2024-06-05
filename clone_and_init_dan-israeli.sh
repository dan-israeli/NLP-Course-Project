# cloning the code from github:
git clone https://github.com/dan-israeli/NLP-Course-Project.git

# refer to the relevant directory
cd NLP-Course-Project/HumanChoicePredictionCode

# create the project's running environment
conda env create -f requirements.yml

# activate the project's running environment
conda activate final_project_env

# run the sweeps of the primary research
python sweeps/PrimaryResearch/new_language_based_strategies_sweep.py
python sweeps/PrimaryResearch/best_new_strategy_strictly_positive_results_sweep.py

# run the sweeps of the secondary research
python sweeps/SecondaryResearch/bert_pca_experiment_sweep.py
