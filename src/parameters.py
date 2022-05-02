from datetime import datetime

# username = input("Enter your username: ")
# engine_depth = int(input("Set the engine depth (1-24): "))
# i_start_y = input("Enter the start year for analysis (e.g. 2020): ")
# i_start_m = input("Enter the start month for analysis (e.g. 01-12): ")
# i_start_datetime = (i_start_y + "-" + i_start_m + "-01" + " 00:00:00")
# start_datetime = datetime.strptime(i_start_datetime, '%Y-%m-%d %H:%M:%S')


class Analyse:
    def __init__(self):
        # Main input parameters
        self.username = input("Enter your username: ")
        self.depth = int(input("Set the engine depth (1-24): "))

        i_start_y = input("Enter the start year (e.g. 2020): ")
        i_start_m = input("Enter the start month (e.g. 01-12): ")
        i_start_datetime = (i_start_y + "-" + i_start_m + "-01" + " 00:00:00")
        self.start_date = datetime.strptime(i_start_datetime, '%Y-%m-%d %H:%M:%S')

        # 


user = Analyse()
print(user.username)
