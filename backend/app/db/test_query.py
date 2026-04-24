from app.db.session import SessionLocal
from app.models import Player


def test_query():
    db = SessionLocal()

    try:
        player = db.query(Player).filter(Player.last_name  == "Jokic").first()

        print("Player:", player)
        print("ID", player.id)
        print("NBA ID:", player.nba_player_id)

        print("\nSeason Stats:")
        for stat in player.season_stats:
            print(stat)

        print("\nGame Stats:")
        for stat in player.game_stats:
            print(stat) 

        

    finally:
        db.close()


if __name__ == "__main__":
    test_query()