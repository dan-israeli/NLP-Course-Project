# imports
from openai import OpenAI
import os
import pandas as pd
import random
import json

# constants
EMPTY = ""

# API keys
CHATGPT_API_KEY = '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'


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

    if sentiment == 'positive':
        if positive_part == "No positive part.":
            return round(random.uniform(0.3, 0.5), 2)

        system_prompt = system_prompt[:111] + " Note that the review you are going to receive is only the positive part of the full review." + system_prompt[111:]
        messages_history = [{"role": "system", "content": system_prompt},
                             {"role": "user", "content": f"{positive_part}"}]

    if sentiment == 'negative':
        if negative_part == "No negative part.":
            return round(random.uniform(0.5, 0.7), 2)

        system_prompt = system_prompt[:111] + " Note that the review you are going to receive is only the negative part of the full review." + system_prompt[111:]
        messages_history = [{"role": "system", "content": system_prompt},
                             {"role": "user", "content": f"{negative_part}"}]

    if sentiment == 'full':
        system_prompt = system_prompt[:111] + " Note that in the review you are going to receive, the positive and negative parts will be separated." + system_prompt[111:]

        user_prompt = f"""Positive part:
                         {positive_part}
                         
                         Negative part:
                         {negative_part}"""

        messages_history = [{"role": "system", "content": system_prompt},
                             {"role": "user", "content": user_prompt}]

    prob = chatgpt(messages_history)
    return prob


def create_prob_file(sentiment, output_file_name):
    with open(output_file_name, "w") as f:
        folder_path = "hotel_reviews/"
        file_lst = os.listdir(folder_path)

        f.write("{\n")

        for file_ind, file in enumerate(file_lst):
            if file_ind % 5 == 0:
                print(f"iteration: {file_ind}")

            df = pd.read_csv(folder_path + file, header=None)
            df = df[[0, 2, 3]]

            for record_ind, (review_ind, positive_part, negative_part) in df.iterrows():
                if pd.isna(positive_part):
                    positive_part = "No positive part."

                if pd.isna(negative_part):
                    negative_part = "No negative part."

                proba2go = get_proba2go(sentiment, positive_part, negative_part)

                f.write(f'"{review_ind}": {proba2go}')
                if file_ind != len(file_lst) - 1 or record_ind != len(df.index) - 1:
                    f.write(f',')
                f.write("\n")

        f.write("}")


def main():
    # with open("positive_proba2go.txt", "r") as f:
    #     st = f.read()
    #
    # nw_dictt = json.loads(st)
    # print(nw_dictt)

    df_lst = []
    folder_path = "hotel_reviews/"
    file_lst = os.listdir(folder_path)

    for file_name in file_lst:
        df = pd.read_csv(f"hotel_reviews/{file_name}", header=None)
        df_lst.append(df)

    # df1 = pd.read_csv("hotel_reviews/1.csv", header=None)
    # df2 = pd.read_csv("hotel_reviews/2.csv", header=None)

    df_concat = pd.concat(df_lst)
    df_concat.reset_index(inplace=True, drop=True)

    # print(df_concat)
    # pd.concat([df1, df2], axis=1)

    df_concat.to_csv("all_reviews.csv")


if __name__ == "__main__":
    main()
