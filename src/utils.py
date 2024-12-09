def annualize(pct: float, days: int) -> float:
   return -1 + (1 + pct) ** (365 / days)
