"""Progress bars for printing analysis progress.

Eventually module to be removed as this will display in the front end.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Progress:
    def bar(
        self, game: int, total: int, start_time: datetime, end_time: datetime
    ) -> None:
        """_summary_

        Args:
            game (int): _description_
            total (int): _description_
            start_time (datetime): _description_
            end_time (datetime): _description_
        """
        avg_game_time = self.timers(start_time, end_time)
        time_r = ((total - (game + 1)) * (avg_game_time)) / 3600
        hours_r = int(time_r)
        if hours_r < 10:
            hrs = "0" + str(hours_r)
        else:
            hrs = str(hours_r)
        mins_tot = (time_r - hours_r) * 60
        mins_r = int(mins_tot)
        if mins_r < 10:
            mins = "0" + str(mins_r)
        else:
            mins = str(mins_r)
        sec_r = int((mins_tot - mins_r) * 60)
        if sec_r < 10:
            secs = "0" + str(sec_r)
        else:
            secs = str(sec_r)
        eta = f"{hrs}:{mins}:{secs}"
        per = 100 * ((game + 1) / float(total))
        bar = "❚" * int(per / 2.5) + "-" * (40 - int(per / 2.5))
        print(
            f"\r|{bar}| {per:.2f}% | ETA: {eta} Game: {game + 1} / {total} ", end="\r"
        )

    def timers(
        self, start_time: datetime, end_time: datetime, time_list: list = []
    ) -> float:
        """Time taken to analyse a chess game - used to calculate the time remaining for analysis.

        Args:
            start_time (datetime): _description_
            end_time (datetime): _description_
            time_list (list, optional): _description_. Defaults to [].

        Returns:
            float: _description_
        """
        analysis_time = end_time - start_time
        time_list.append(analysis_time)
        avg_game_time = sum(time_list) / len(time_list)
        return avg_game_time
