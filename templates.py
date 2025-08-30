import os, random

def pick_niche():
    allowed = os.getenv("NICHES","motivation,facts,list,relationship").split(",")
    allowed = [a.strip().lower() for a in allowed if a.strip()]
    return random.choice(allowed)

def build(niche: str):
    cta = os.getenv("CTA", "follow for more → @yourchannel")
    if niche == "motivation":
        lines = [
            "stop scrolling.",
            "your future self is watching.",
            "make them proud."
        ] + ([cta] if os.getenv("ADD_CTA","1") == "1" else [])
        queries = ["athlete training", "city night bokeh", "mountain sunrise", "boxing gym"]
        title = "this will change your day 💯"
        desc = "daily discipline > random motivation.\n" + cta
        tags = ["motivation","discipline","success","shorts"]
        return queries, lines, title, desc, tags

    if niche == "facts":
        fact = random.choice([
            "Octopuses have three hearts and blue blood.",
            "Honey never spoils—edible jars were found in ancient tombs.",
            "A day on Venus is longer than a year on Venus.",
            "Sharks existed before trees."
        ])
        lines = ["did you know?", fact] + ([cta] if os.getenv("ADD_CTA","1") == "1" else [])
        queries = ["science lab", "ocean waves closeup", "star field timelapse"]
        title = "5 seconds of knowledge 🤯"
        desc = fact + "\n" + cta
        tags = ["facts","trivia","learn","shorts"]
        return queries, lines, title, desc, tags

    if niche == "list":
        items = ["Pay yourself first","Automate savings","Track every dollar","Avoid impulse buys","Invest consistently"]
        lines = ["top 5 money habits"] + [f"{i+1}. {it}" for i,it in enumerate(items)] + ([cta] if os.getenv("ADD_CTA","1") == "1" else [])
        queries = ["keyboard typing closeup", "city timelapse night", "coffee shop broll"]
        title = "top 5 money habits to start now ✅"
        desc = ", ".join(items) + "\n" + cta
        tags = ["money","habits","lifehacks","shorts"]
        return queries, lines, title, desc, tags

    if niche == "relationship":
        quote = random.choice([
            "Choose people who choose you.",
            "Consistency is love’s language.",
            "Boundaries are self-respect in action.",
            "You deserve the same love you give."
        ])
        lines = [quote] + ([cta] if os.getenv("ADD_CTA","1") == "1" else [])
        queries = ["rain on window", "candle flame closeup", "sunset silhouettes"]
        title = "read this twice. ❤️"
        desc = quote + "\n" + cta
        tags = ["love","relationship","quotes","shorts"]
        return queries, lines, title, desc, tags

    # default
    return ["city night"], ["keep going.", cta], "keep going.", cta, ["shorts"]
