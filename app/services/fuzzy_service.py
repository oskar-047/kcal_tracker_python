from rapidfuzz import process, fuzz
import unicodedata, re
from repositories.interfaces import FoodRepo
from domain.food import Food

def fuzzy_search(key, foods: list[Food], limit: int) -> tuple[list[Food], list[float]]:
    
    fav_boost: int = 40

    if not key:
        return foods, []

    key = normalize(key)

    scorer, cutoff = get_scorer(key)

    choices = [normalize(food.name) for food in foods]

    results = process.extract(
        key,
        choices,
        scorer=scorer,
        score_cutoff=cutoff-fav_boost,
        limit=limit
    )

    food_items = []
    for _, score, i in results:
        score = score+fav_boost if foods[i].favorite == 1 else score
        if score < cutoff: continue
        food_items.append({
            "food": foods[i],
            "score": score
        })
    
    food_items.sort(key=lambda x:x["score"], reverse=True)

    result_foods = [i["food"] for i in food_items]
    result_scores = [i["score"] for i in food_items]

    return result_foods, result_scores

    print(results)

    # for
    # results: [(matched_name, score, original_item), ...]
    # result_foods = [foods[i] for _, score, i in results if score]
    # result_scores = [score for _, score, _ in results]
    # return result_foods, result_scores
    return [], []





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
