# imports
from openai import OpenAI
import pandas as pd
import random
import os
import json

# constants
EMPTY = ""

# API keys
CHATGPT_API_KEY = 'please enter your API key'


def chatgpt(messages_history):
    """
    Get messages history of the conversation with the model, and return
    the model's response to it.
    """
    client = OpenAI(api_key=CHATGPT_API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_history
    )

    return response.choices[0].message.content


def get_proba2go(sentiment, positive_part, negative_part):
    system_prompt = f"""You are a hotel recommender on Booking.com. That is, you are going to receive a hotel review from that website. Based on the review you receive, you should give a probability, between 0 and 1, that the overall score of the hotel is at least 8. Your answer should only be the probability, in float format. Remember that the review represents a subjective experience."""

    # only the positive part is provided to the LLM
    if sentiment == 'positive':
        # if the positive part provided is missing
        if positive_part == "No positive part.":
            # sample uniformly in the range [0.3, 0.5] (expected value is 0.4 < 0.5)
            return round(random.uniform(0.3, 0.5), 2)

        # provide the positive part to the LLM
        system_prompt = system_prompt[:111] + " Note that the review you are going to receive is only the positive part of the full review." + system_prompt[111:]
        messages_history = [{"role": "system", "content": system_prompt},
                             {"role": "user", "content": f"{positive_part}"}]

    # only the negative part is provided to the LLM
    if sentiment == 'negative':
        # if the negative part provided is missing
        if negative_part == "No negative part.":
            # sample uniformly in the range [0.3, 0.5] (expected value is 0.6 > 0.5)
            return round(random.uniform(0.5, 0.7), 2)

        # provide the negative part to the LLM
        system_prompt = system_prompt[:111] + " Note that the review you are going to receive is only the negative part of the full review." + system_prompt[111:]
        messages_history = [{"role": "system", "content": system_prompt},
                             {"role": "user", "content": f"{negative_part}"}]

    # the entrie review is provided to the LLM (both positive and negative parts)
    if sentiment == 'full':
        system_prompt = system_prompt[:111] + " Note that in the review you are going to receive, the positive and negative parts will be separated." + system_prompt[111:]

        user_prompt = f"""Positive part:
                         {positive_part}
                         
                         Negative part:
                         {negative_part}"""

        messages_history = [{"role": "system", "content": system_prompt},
                             {"role": "user", "content": user_prompt}]

    # get the LLM response (the probability of the given review)
    prob = chatgpt(messages_history)
    return prob


def create_prob_file(sentiment, output_file_name):
    """
    Getting the sentiment (positive, negative or full),
    and creating the corresponding .txt probabilities file
    """
    with open(output_file_name, "w") as f:
        f.write("{\n")

        df = pd.read_csv("all_reviews.csv")
        df = df[['0', '2', '3']]

        for record_ind, (review_ind, positive_part, negative_part) in df.iterrows():
            # replace nan value of the positive part with the string "No positive part"
            if pd.isna(positive_part):
                positive_part = "No positive part."

            # replace nan value of the negative part with the string "No negative part"
            if pd.isna(negative_part):
                negative_part = "No negative part."

            proba2go = get_proba2go(sentiment, positive_part, negative_part)

            f.write(f'"{review_ind}": {proba2go}')
            if record_ind != len(df.index) - 1:
                f.write(f',')
            f.write("\n")

        f.write("}")


def main():

    # create the 'positive_proba2go.txt' file
    create_prob_file("positive", "positive_proba2go.txt")

    # create the 'negative_proba2go.txt' file
    create_prob_file("negative", "negative_proba2go.txt")

    # create the 'baseline_proba2go.txt' file
    create_prob_file("full", "baseline_proba2go.txt")



if __name__ == "__main__":
    main()
