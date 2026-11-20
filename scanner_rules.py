from dataclasses import dataclass
from datetime import datetime, time
from typing import List

@dataclass
class Candle:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

def candle_color(c: Candle) -> str:
    if c.close > c.open:
        return "GREEN"
    if c.close < c.open:
        return "RED"
    return "DOJI"

def pct_move(start: float, end: float) -> float:
    return abs(end - start) / start * 100 if start else 0.0

def scan_setups(candles: List[Candle], direction: str, pdh: float, pdl: float):
    """Input candles oldest-first; use completed 5-minute candles only."""
    alerts = []
    if len(candles) < 2:
        return alerts

    # Setup 1: within first three session candles, opposite candle to market/stock direction.
    # LONG/upside => RED; SHORT/downside => GREEN.
    for i in range(1, min(len(candles), 3)):
        prev, cur = candles[i-1], candles[i]
        required_color = "RED" if direction == "LONG" else "GREEN"
        if candle_color(cur) == required_color:
            open_inside = prev.low <= cur.open <= prev.high
            close_inside = prev.low <= cur.close <= prev.high
            if open_inside and close_inside:
                alerts.append({
                    "setup": "SETUP 1",
                    "time": cur.ts.strftime("%H:%M"),
                    "detail": "Opposite-colour candle; Open & Close inside previous candle High-Low",
                    "trigger_close": cur.close,
                })

    # Setup 2: first 2 candles only. First candle crosses PDH for LONG or PDL for SHORT.
    if len(candles) >= 2:
        c1, c2 = candles[0], candles[1]
        if direction == "LONG":
            crossed = c1.high > pdh
        else:
            crossed = c1.low < pdl
        combined = pct_move(c1.open, c2.close)
        second = pct_move(c2.open, c2.close)
        if crossed and combined <= 2.5 and second <= 1.0:
            alerts.append({
                "setup": "SETUP 2",
                "time": c2.ts.strftime("%H:%M"),
                "detail": f"First 2 candles; total move {combined:.2f}%; candle 2 move {second:.2f}%",
                "trigger_close": c2.close,
            })

    # Setup 3: ignore first three candles; until 11:00, current candle must be opposite
    # colour and have volume strictly lower than every previous completed same-day candle.
    for i in range(3, len(candles)):
        cur = candles[i]
        if cur.ts.time() > time(11, 0):
            continue
        prior = candles[:i]
        if not prior or not all(cur.volume < p.volume for p in prior):
            continue
        required_color = "RED" if direction == "LONG" else "GREEN"
        if candle_color(cur) == required_color:
            alerts.append({
                "setup": "SETUP 3",
                "time": cur.ts.strftime("%H:%M"),
                "detail": f"Opposite-colour candle with lowest volume so far ({cur.volume:g})",
                "trigger_close": cur.close,
            })

    # One alert per setup/time, retain order.
    unique, seen = [], set()
    for item in alerts:
        key = (item["setup"], item["time"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique

def eligible(change_pct: float, direction: str, advances: int, declines: int):
    if abs(change_pct) > 5:
        return False
    if direction == "LONG":
        return advances > declines and change_pct > 0
    if direction == "SHORT":
        return declines > advances and change_pct < 0
    return False
