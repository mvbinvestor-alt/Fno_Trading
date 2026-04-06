from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SignalType(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class MarketRegime(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"

class Signal(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    stock: str
    signal_type: SignalType
    entry: float
    stop_loss: float
    target_1: float
    target_2: float
    position_size: int
    confidence_score: float
    reasons: List[str]
    sector: str
    market_regime: MarketRegime
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "ACTIVE"
    
class Trade(BaseModel):
    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    signal_id: str
    stock: str
    signal_type: SignalType
    entry_price: float
    stop_loss: float
    target_1: float
    target_2: float
    position_size: int
    entry_time: datetime
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    pnl: Optional[float] = None
    status: str = "OPEN"

class MarketData(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    timestamp: datetime
    vwap: Optional[float] = None
    
class OptionChainData(BaseModel):
    symbol: str
    strike: float
    call_oi: int
    put_oi: int
    call_oi_change: int
    put_oi_change: int
    pcr: float
    timestamp: datetime