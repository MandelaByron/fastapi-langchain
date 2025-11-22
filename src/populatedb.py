import json
from sqlmodel import Session
from src.players.models import Players
from src.database import engine


from dateutil import parser

def parse_date(s):
    if not s:
        return None
    try:
        return parser.parse(s, dayfirst=True).date()
    except Exception:
        return None
def remove_duplicates(data):
    seen = set()
    unique_data = []
    for item in data:
        # Define a unique key, such as 'id' or a tuple of values that uniquely identify a player
        unique_key = item["id"]  # Change this to the field that uniquely identifies a player
        if unique_key not in seen:
            seen.add(unique_key)
            unique_data.append(item)
    return unique_data

def populate_db(json_file: str):
    with open(json_file, "r") as file:
        data = json.load(file)
    data = remove_duplicates(data)
    with Session(engine) as session:
        for item in data:
            item["date_of_birth"] = parse_date(item["date_of_birth"])
            item["joined_date"] = parse_date(item["joined_date"])
            item["contract_expires"] = parse_date(item["contract_expires"])
            player = Players(**item)
            session.add(player)
        session.commit()
        print("Database populated successfully!")

populate_db("/home/byron/Desktop/code/scrapy_docker/player_data.json")