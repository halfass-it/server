from dataclasses import dataclass
import datetime


@dataclass
class Date:
  date: str = None

  def now(self):
    self.date = Date(datetime.datetime.now().strftime('%H-%M-%S_%d-%m-%Y'))
    return self.date

  def __str__(self):
    return self.date

  def __bytes__(self):
    return self.date.encode('utf-8')
