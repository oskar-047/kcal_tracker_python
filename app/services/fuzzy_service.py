from rapidfuzz import process, fuzz
import unicodedata, re
from repositories.interfaces import FoodRepo
from domain.food import Food

def fuzzy_search(key, foods: list[Food], limit: int) -> tuple[list[Food], list[float]]:
    
    key = normalize(key)

    scorer, cutoff = get_scorer(key)

    choices = [normalize(food.name) for food in foods]

    results = process.extract(
        key,
        choices,
        scorer=scorer,
        score_cutoff=cutoff,
        limit=limit
    )
    # results: [(matched_name, score, original_item), ...]
    result_foods = [foods[i] for _, score, i in results if score]
    result_scores = [score for _, score, _ in results]
    return result_foods, result_scores





def get_scorer(query: str):
    lenght = len(query)

    if lenght < 3:
        return fuzz.partial_ratio, 85

    if lenght < 5:
        return fuzz.WRatio, 70

    return fuzz.WRatio, 60


def normalize(text: str) -> str:
    text = text.strip().lower()                # trim + lowercase
    text = unicodedata.normalize("NFKC", text) # unify unicode forms (keeps accents)
    text = re.sub(r"[-_/]+", " ", text)        # replace separators with space
    text = re.sub(r"\s+", " ", text)           # collapse spaces
    return text
