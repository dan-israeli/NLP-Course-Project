# NLP Course Project 🤖📝

## Contents
- [Running Instructions](#running-instructions)
  - [Recreate Experiments Results](#recreate-experiments-results)
  - [Primary Research - Recreating the proba2go Files](#primary-research---recreating-the-proba2go-files)
  - [Secondary Research - Recreating the BERT PCA Embeddings Files](#secondary-research---recreating-the-bert-pca-embeddings-files)

## Running Instructions

### Recreate Experiments Results

The experiments in our project were executed and tracked using the Weights & Biases platform.

To recreate an experiment (sweep) on your local machine, follow these steps:

1. **Log in to Weights & Biases (W&B)** 

   Use the following command to log in to your W&B account:
    ```bash
    wandb login
    ```

   *Note that you can create an account in the following [link](https://wandb.ai/site).

2. **Clone the repository**

   Use the following command to clone the repository to your local machine using Git:
   
   ```bash
   git clone https://github.com/dan-israeli/NLP-Course-Project
    ```
4. **Create and activate the conda environment**

    After cloning the repository, navigate into the project code directory:

    ```bash
    cd NLP-Course-Project/HumanChoicePredictionCode
    ```

    Then, use the following command to create a conda environment from the requirements.yml file provided in the project:
    ```bash
    conda env create -f requirements.yml
    ```

5. **Activate the environment**

    Now, use the following command to activate the created environment:
    ```bash
    conda activate final_project_env
    ```
6. **Running an experiment**

    Finally, use the following command to run an experiment (sweep):

   ```bash
    python <sweep_file_path>
    ```
    Where <sweep_file_path> is one of the following paths:

    - sweeps/PrimaryResearch/new_language_based_strategies_sweep.py
    - sweeps/PrimaryResearch/best_new_strategy_(strictly_positive)_results_sweep.py
    - sweeps/SecondaryResearch/bert_pca_experiment_sweep.py

    Then, follow the instructions presented in the terminal.
    
    *Choose the path according to the experiment you would like to run.

**Optional shortcut**

As a shortcut to execute steps 2-5, and to run **all** of the experiments, follow the steps below:

1. Download the provided "clone_and_init_dan-israeli.sh" file (from the repository's main directory).
2. Open the terminal and run the following command:
    
   ```bash
   source <file_path>
   ```

   Where <file_path> is the path of the downloaded file on your local machine.

3. Follow the instructions presented in the terminal.

### Primary Research - Recreating the proba2go Files

The new proba2go files that were created for our experiments, and are required to run the code, are as follows:

- positive_proba2go.txt
- negative_proba2go.txt
- baseline_proba2go.txt

These files are provided in this repository (in the appropriate directories).

Regardless, to recreate them, follow the steps below:

1. Download the provided "LLM_proba2go.py" Python file (in the "primary research/proba2go" directory).
2. Add the provided "all_reviews.csv" file (in the "primary research/proba2go" directory) to the directory where the Python file is placed (on your local machine).
3. Enter your OpenAI API key in the designated line at the top of the Python file:

   ![image](https://github.com/dan-israeli/NLP-Course-Project/assets/127883151/e278b9c1-0c73-4186-89c4-c5169b632fd4)

    *Note that you can create an OpenAI API key in the following [link](https://openai.com/blog/openai-api).

4. Run the Python file to receive the mentioned proba2go files.

### Secondary Research - Recreating the BERT PCA Embeddings Files

The new BERT PCA embeddings files that were created for our experiments, and are required to run the code, are as follows:

BERT_PCA_{i}.csv (for i = 5, 10, ... 250)

These files are provided in this repository (in the appropriate directories).

Regardless, to recreate them, follow the steps below:

1. Download the provided .ipynb notebook (in the "Notebooks_dan-israeli" directory).
2. Run all the code blocks under the "Creating the PCA Embeddings for the Tested Dimensions" section according to the notebook's instructions.
