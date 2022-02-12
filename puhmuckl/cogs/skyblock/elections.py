import requests, json
from util import config
import cogs.skyblock.util as util
from datetime import datetime

class Perk:
    def __init__(self, name: str, desc: str):
        
        self.name = util.deminecraftify(name)
        self.description = util.deminecraftify(desc)


class Candidate:
    def __init__(self, key: str, name: str, votes: int):
        self.key = util.deminecraftify(key).capitalize()
        self.name = util.deminecraftify(name)
        self.votes = votes
        self.perks = []

    def add_perk(self, perk: Perk):
        self.perks.append(perk)


class Election:
    def __init__(self, year: int):
        self.year = year
        self.candidates = []

    def add_candidate(self, candidate: Candidate):
        self.candidates.append(candidate)


class ElectionRequest:
    API_ENDPOINT = "https://api.hypixel.net/resources/skyblock/election"

    def __init__(self):
        self.success = False
        self.mayor = None
        self.current_election = None

        self.query()

    def query(self):
        response = requests.get(ElectionRequest.API_ENDPOINT)
        if not response.ok:
            return

        data = json.loads(response.text)
        if not data["success"]:
            return

        self.last_updated = datetime.utcfromtimestamp(data["lastUpdated"] / 1000)
        
        self.mayor = Candidate(data["mayor"]["key"], data["mayor"]["name"], 0)
        for perk in data["mayor"]["perks"]:
            self.mayor.add_perk(Perk(perk["name"], perk["description"]))

        if "current" not in data:
            return
        
        self.current_election = Election(data["current"]["year"])

        for candidate in data["current"]["candidates"]:
            candidate_obj = Candidate(candidate["key"], candidate["name"], candidate["votes"])
            for perk in candidate["perks"]:
                candidate_obj.add_perk(Perk(perk["name"], perk["description"]))

            self.current_election.add_candidate(candidate_obj)
  