import numpy as np
import json

################################
# CONSTS
################################

REVIEWS = 0
BOT_ACTION = 1
USER_DECISION = 2

def load_dict(path):
    # loas the initial dictionary
    file = open(path, "r").read()
    init_dict = json.loads(file)

    # cast the keys into integers
    dict = {int(k): v for k, v in init_dict.items()}

    return dict

# load the proba2go txt files and convert them to dictionaries
ORIGINAL_DICT = load_dict("data/LLM_proba2go/original_proba2go.txt")
POSITIVE_DICT = load_dict("data/LLM_proba2go/positive_proba2go.txt")
NEGATIVE_DICT = load_dict("data/LLM_proba2go/negative_proba2go.txt")
FULL_DICT = load_dict("data/LLM_proba2go/baseline_proba2go.txt")

################################

def correct_action(information):
    if information["hotel_value"] >= 8:
        return 1
    else:
        return 0


def random_action(information):
    return np.random.randint(2)


def user_rational_action(information):
    if information["bot_message"] >= 8:
        return 1
    else:
        return 0


def user_picky(information):
    if information["bot_message"] >= 9:
        return 1
    else:
        return 0


def user_sloppy(information):
    if information["bot_message"] >= 7:
        return 1
    else:
        return 0


def user_short_t4t(information):
    if len(information["previous_rounds"]) == 0 \
            or (information["previous_rounds"][-1][BOT_ACTION] >= 8 and
                information["previous_rounds"][-1][REVIEWS].mean() >= 8) \
            or (information["previous_rounds"][-1][BOT_ACTION] < 8 and
                information["previous_rounds"][-1][REVIEWS].mean() < 8):  # cooperation
        if information["bot_message"] >= 8:  # good hotel
            return 1
        else:
            return 0
    else:
        return 0


def user_picky_short_t4t(information):
    if information["bot_message"] >= 9 or ((information["bot_message"] >= 8) and (
            len(information["previous_rounds"]) == 0 or (
            information["previous_rounds"][-1][REVIEWS].mean() >= 8))):  # good hotel
        return 1
    else:
        return 0


def user_hard_t4t(information):
    if len(information["previous_rounds"]) == 0 \
            or np.min(np.array([((r[BOT_ACTION] >= 8 and r[REVIEWS].mean() >= 8)
                                 or (r[BOT_ACTION] <= 8 and r[REVIEWS].mean() < 8)) for r in
                                information["previous_rounds"]])) == 1:  # cooperation
        if information["bot_message"] >= 8:  # good hotel
            return 1
        else:
            return 0
    else:
        return 0


def history_and_review_quality(history_window, quality_threshold):
    def func(information):
        if len(information["previous_rounds"]) == 0 \
                or history_window == 0 \
                or np.min(np.array([((r[BOT_ACTION] >= 8 and r[REVIEWS].mean() >= 8)
                                     or (r[BOT_ACTION] <= 8 and r[REVIEWS].mean() < 8)) for r in
                                    information["previous_rounds"][
                                    -history_window:]])) == 1:  # cooperation from *result's* perspective
            if information["bot_message"] >= quality_threshold:  # good hotel from user's perspective
                return 1
            else:
                return 0
        else:
            return 0
    return func


def topic_based(positive_topics, negative_topics, quality_threshold):
    def func(information):
        review_personal_score = information["bot_message"]
        for rank, topic in enumerate(positive_topics):
            review_personal_score += int(information["review_features"][topic])*2/(rank+1)
        for rank, topic in enumerate(negative_topics):
            review_personal_score -= int(information["review_features"][topic])*2/(rank+1)
        if review_personal_score >= quality_threshold:  # good hotel from user's perspective
            return 1
        else:
            return 0
    return func


def LLM_based(is_stochastic):

    if is_stochastic:
        def func(information):
            review_llm_score = ORIGINAL_DICT[information["review_id"]]
            return int(np.random.rand() <= review_llm_score)
        return func
    else:
        def func(information):
            review_llm_score = ORIGINAL_DICT[information["review_id"]]
            return int(review_llm_score >= 0.5)
        return func


# Strictly Positive strategy
def LLM_positive(information):
    review_id = information["review_id"]

    p = float(POSITIVE_DICT[review_id])
    return int(np.random.rand() <= p)

# Strictly Negative strategy
def LLM_negative(information):
    review_id = information["review_id"]

    p = float(NEGATIVE_DICT[review_id])
    return int(np.random.rand() <= p)

# Baseline strategy
def LLM_full(information):
    review_id = information["review_id"]

    p = float(FULL_DICT[review_id])
    return int(np.random.rand() <= p)
