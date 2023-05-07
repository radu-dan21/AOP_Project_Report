from src.service import Service


def get_weather_stations_and_subscribed_users() -> None:
    stations_and_users: dict = Service.get_weather_stations_and_subscribed_users()
    if not stations_and_users:
        print("\nThere are no stations!")
    else:
        print("\nSubscriptions:")
        for station, station_users in stations_and_users.items():
            print(f"\n{str(station)}")
            if not station_users:
                print("\tNo subscribed users")
            else:
                for user in station_users:
                    print(f"\t{str(user)}")
