"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = [
    # ── Standard profiles ───────────────────────────────────────────
    {
        "name": "Default Pop / Happy",
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    },
    {
        "name": "High-Energy Pop",
        "favorite_genre": "pop",
        "favorite_mood": "intense",
        "target_energy": 0.93,
        "likes_acoustic": False,
    },
    {
        "name": "Chill Lofi",
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
    {
        "name": "Deep Intense Rock",
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.91,
        "likes_acoustic": False,
    },
    # ── Adversarial / edge-case profiles ────────────────────────────
    {
        # Conflicting: sad mood but extreme high energy.
        # No song in the catalog is both sad AND high-energy, so every
        # result has to sacrifice either mood or energy — max possible
        # score is ~0.70.  Tests whether the scorer degrades gracefully
        # instead of silently promoting a wrong match.
        "name": "[EDGE] Sad Bangers",
        "favorite_genre": "blues",
        "favorite_mood": "sad",
        "target_energy": 0.95,
        "likes_acoustic": False,
    },
    {
        # Ghost genre: "k-pop" does not exist in the catalog, so
        # genre_contrib is always 0.0.  The top results win purely on
        # mood + energy + acoustic — genre match (worth 0.35) is dead
        # weight.  Maximum achievable score is 0.65.
        "name": "[EDGE] Ghost Genre (k-pop)",
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    },
    {
        # Contradictory acoustic preference: the user wants electronic /
        # euphoric music (inherently non-acoustic) but also likes_acoustic.
        # The best genre+mood match (Bassline District, acousticness 0.03)
        # will be penalised on the acoustic dimension, while highly
        # acoustic songs score well acoustically but miss genre and mood.
        "name": "[EDGE] Acoustic Electronic",
        "favorite_genre": "electronic",
        "favorite_mood": "euphoric",
        "target_energy": 0.92,
        "likes_acoustic": True,
    },
]


def print_recommendations(profile: dict, recommendations: list) -> None:
    width = 62
    name = profile["name"]
    genre = profile["favorite_genre"]
    mood = profile["favorite_mood"]
    energy = profile["target_energy"]
    acoustic = "acoustic" if profile["likes_acoustic"] else "non-acoustic"

    print("\n" + "=" * width)
    print(f"  {name}".ljust(width))
    print(f"  {genre} / {mood} | energy {energy} | {acoustic}".ljust(width))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Reasons:")
        for reason in explanation.split(", "):
            print(f"         • {reason}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        recommendations = recommend_songs(profile, songs, k=5)
        print_recommendations(profile, recommendations)


if __name__ == "__main__":
    main()
