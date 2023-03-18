import secrets
import string
from time import time
from database.db_functions import insert_token,get_tokens
TYPES =  ["one_month","three_months", "six_months", "one_year"] 

def generate_token(length=32):
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token

def generate_tokens(amount, length=32):
    return [generate_token(length) for _ in range(amount)]

def generate_all():
    # Generate 500 tokens for each subscription type
    three_months_tokens = generate_tokens(173)
    six_months_tokens = generate_tokens(500)
    one_year_tokens = generate_tokens(500)

    tokens_tabs = [three_months_tokens, six_months_tokens, one_year_tokens]
    start_time = int(time())
    inserted_tokens = 0
    for token_tab, type in zip(tokens_tabs, TYPES):
        for token in token_tab:
            if inserted_tokens%100 == 0 and inserted_tokens != 0:
                remaining_time = (int(time()) - start_time) / inserted_tokens * (1173 - inserted_tokens)
                print("Inserted " + str(inserted_tokens) + " tokens. Remaining time: " + str(remaining_time) + " seconds")
            insert_token(token, str(type))
            inserted_tokens += 1
        print("Finished generating tokens for " + str(type) + " subscription")


def write_tokens_to_csv():
    import csv
    with open("tokens.csv", "w", newline="") as file:
        # Fetch the tokens from the database
        three_months_tokens = get_tokens("three_months")
        six_months_tokens = get_tokens("six_months")
        one_year_tokens = get_tokens("one_year")
        one_month_tokens = get_tokens("one_month")
        tokens = [one_month_tokens,three_months_tokens, six_months_tokens, one_year_tokens ]
        
        # Insert the token with the type into the CSV file, with the token type
        writer = csv.writer(file)
        writer.writerow(["token", "type"])
        for token_tab, type in zip(tokens, TYPES):
            for token in token_tab:
                writer.writerow([token[0], type])

write_tokens_to_csv()