from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from config import config
from models import Signal, SignalType, MarketRegime
from signal_generator import SignalGenerator
from scheduler.tasks import TradingScheduler
from backtest.engine import backtest_engine
from services.market_data import market_data_client
from services.position_sizing import position_sizer

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize components
signal_generator = SignalGenerator(db)
scheduler = TradingScheduler(signal_generator)

# Create FastAPI app
app = FastAPI(title="F&O Trading System API")
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============== Models ==============

class GenerateSignalsRequest(BaseModel):
    manual: bool = True

class BacktestRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    capital: float = 500000

class UpdateCapitalRequest(BaseModel):
    capital: float

class SchedulerControlRequest(BaseModel):
    action: str  # "start" or "stop"

# ============== API Routes ==============

@api_router.get("/")
async def root():
    return {"message": "F&O Trading System API", "status": "active"}

@api_router.get("/health")
async def health_check():
    """System health check"""
    try:
        # Check database connection
        await db.command('ping')
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "scheduler": scheduler.is_running,
        "timestamp": datetime.now().isoformat()
    }

@api_router.post("/signals/generate")
async def generate_signals(request: GenerateSignalsRequest, background_tasks: BackgroundTasks):
    """Generate trading signals manually or via background task"""
    try:
        if request.manual:
            # Generate immediately
            signals = await signal_generator.generate_signals()
            return {
                "status": "success",
                "signals_count": len(signals),
                "signals": [s.model_dump() for s in signals]
            }
        else:
            # Generate in background
            background_tasks.add_task(signal_generator.generate_signals)
            return {
                "status": "queued",
                "message": "Signal generation queued in background"
            }
    except Exception as e:
        logger.error(f"Error generating signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/signals")
async def get_signals(limit: int = 50, status: str = "ACTIVE"):
    """Get recent trading signals"""
    try:
        query = {}
        if status:
            query['status'] = status
        
        signals = await db.signals.find(query, {"_id": 0}).sort("timestamp", -1).limit(limit).to_list(limit)
        return {
            "status": "success",
            "count": len(signals),
            "signals": signals
        }
    except Exception as e:
        logger.error(f"Error fetching signals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/signals/{signal_id}")
async def get_signal(signal_id: str):
    """Get specific signal by ID"""
    try:
        signal = await db.signals.find_one({"id": signal_id}, {"_id": 0})
        if not signal:
            raise HTTPException(status_code=404, detail="Signal not found")
        return signal
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching signal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/market/regime")
async def get_market_regime():
    """Get current market regime"""
    try:
        from services.regime_detection import regime_detector
        
        regime = regime_detector.get_current_regime()
        return {
            "regime": regime,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching market regime: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/market/sectors")
async def get_sector_strength():
    """Get sector strength analysis"""
    try:
        from services.sector_strength import sector_analyzer
        
        return {
            "sectors": sector_analyzer.sector_strength,
            "top_sectors": sector_analyzer.get_top_sectors(3),
            "weak_sectors": sector_analyzer.get_weakest_sectors(3),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching sector strength: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/backtest/run")
async def run_backtest(request: BacktestRequest):
    """Run backtest on historical data"""
    try:
        # Get historical signals
        signals_data = await db.signals.find({}, {"_id": 0}).limit(100).to_list(100)
        
        if not signals_data:
            return {
                "status": "error",
                "message": "No signals found for backtesting"
            }
        
        # Convert to Signal objects
        signals = []
        for s in signals_data:
            try:
                if isinstance(s.get('timestamp'), str):
                    s['timestamp'] = datetime.fromisoformat(s['timestamp'])
                signal = Signal(**s)
                signals.append(signal)
            except Exception as e:
                logger.error(f"Error converting signal: {e}")
                continue
        
        # Run backtest
        results = backtest_engine.run_backtest(signals, {})
        
        # Save results
        result_doc = {
            "timestamp": datetime.now().isoformat(),
            "metrics": results.get('metrics', {}),
            "total_trades": results.get('total_trades', 0),
            "initial_capital": request.capital,
            "final_capital": results.get('final_capital', request.capital)
        }
        await db.backtest_results.insert_one(result_doc)
        
        return {
            "status": "success",
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Backtest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/backtest/results")
async def get_backtest_results(limit: int = 10):
    """Get recent backtest results"""
    try:
        results = await db.backtest_results.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit).to_list(limit)
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error fetching backtest results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/trades")
async def get_trades(limit: int = 50):
    """Get trade history"""
    try:
        trades = await db.trades.find({}, {"_id": 0}).sort("entry_time", -1).limit(limit).to_list(limit)
        return {
            "status": "success",
            "count": len(trades),
            "trades": trades
        }
    except Exception as e:
        logger.error(f"Error fetching trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/analytics/performance")
async def get_performance_analytics():
    """Get performance analytics"""
    try:
        # Get all completed trades
        trades = await db.trades.find({"status": "CLOSED"}, {"_id": 0}).to_list(1000)
        
        if not trades:
            return {
                "status": "success",
                "message": "No completed trades yet",
                "metrics": {}
            }
        
        # Calculate metrics
        winning_trades = [t for t in trades if t.get('pnl', 0) > 0]
        losing_trades = [t for t in trades if t.get('pnl', 0) <= 0]
        
        win_rate = (len(winning_trades) / len(trades)) * 100 if trades else 0
        total_pnl = sum([t.get('pnl', 0) for t in trades])
        
        return {
            "status": "success",
            "metrics": {
                "total_trades": len(trades),
                "winning_trades": len(winning_trades),
                "losing_trades": len(losing_trades),
                "win_rate": round(win_rate, 2),
                "total_pnl": round(total_pnl, 2),
                "avg_win": round(sum([t['pnl'] for t in winning_trades]) / len(winning_trades), 2) if winning_trades else 0,
                "avg_loss": round(sum([t['pnl'] for t in losing_trades]) / len(losing_trades), 2) if losing_trades else 0
            }
        }
    except Exception as e:
        logger.error(f"Error calculating analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/config/capital")
async def update_capital(request: UpdateCapitalRequest):
    """Update trading capital"""
    try:
        position_sizer.update_capital(request.capital)
        return {
            "status": "success",
            "capital": request.capital
        }
    except Exception as e:
        logger.error(f"Error updating capital: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/scheduler/control")
async def control_scheduler(request: SchedulerControlRequest):
    """Start or stop the scheduler"""
    try:
        if request.action == "start":
            scheduler.start()
            return {"status": "success", "message": "Scheduler started"}
        elif request.action == "stop":
            scheduler.stop()
            return {"status": "success", "message": "Scheduler stopped"}
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'")
    except Exception as e:
        logger.error(f"Scheduler control error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/scheduler/status")
async def get_scheduler_status():
    """Get scheduler status"""
    try:
        status = scheduler.get_status()
        return {
            "status": "success",
            "scheduler": status
        }
    except Exception as e:
        logger.error(f"Error getting scheduler status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/system/status")
async def get_system_status():
    """Get overall system status"""
    try:
        # Check 5paisa connection
        fivepaisa_status = "configured" if config.FIVEPAISA_USER_KEY else "not_configured"
        
        # Check Telegram
        telegram_status = "configured" if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID else "not_configured"
        
        # Check Email
        email_status = "configured" if config.GMAIL_SENDER and config.GMAIL_APP_PASSWORD else "not_configured"
        
        return {
            "status": "success",
            "system": {
                "fivepaisa_api": fivepaisa_status,
                "telegram": telegram_status,
                "email": email_status,
                "scheduler": scheduler.is_running,
                "database": "connected"
            }
        }
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Include router in app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Starting F&O Trading System...")
    # Initialize market data client
    await market_data_client.initialize()
    logger.info("System started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down F&O Trading System...")
    scheduler.stop()
    await market_data_client.close()
    client.close()
    logger.info("System shutdown complete")
