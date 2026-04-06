# F&O Trading System - Indian Stock Market Signal Generator

Production-grade algorithmic trading system for NSE F&O intraday trading with automated signal generation, Telegram alerts, and backtesting.

## Features

- 🎯 Multi-factor signal generation (Price Action + Volume + Option Chain + Sector + Market Regime)
- 📱 Telegram alerts for trade signals
- 📊 Real-time trading dashboard
- 🔄 Automated scheduler (every 5 minutes during market hours)
- 📈 Backtesting engine with performance metrics
- 💰 Risk-based position sizing (1% risk per trade)
- 🏦 5paisa API integration
- 📉 Market regime detection (BULLISH/BEARISH/SIDEWAYS)
- 🎨 Professional Bloomberg-style dashboard

## Tech Stack

**Backend:**
- FastAPI
- MongoDB
- Python 3.11+
- py5paisa API
- python-telegram-bot

**Frontend:**
- React
- Tailwind CSS
- Recharts
- Axios

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (local or Atlas)

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

Backend runs on: `http://localhost:8001`

### 3. Frontend Setup

```bash
cd frontend
npm install
echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
npm start
```

Frontend runs on: `http://localhost:3000`

## Configuration

### Backend .env

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=trading_system

# 5paisa API
FIVEPAISA_APP_NAME=your_app_name
FIVEPAISA_APP_SOURCE=your_app_source
FIVEPAISA_USER_ID=your_user_id
FIVEPAISA_USER_PASSWORD=your_password
FIVEPAISA_USER_KEY=your_api_key
FIVEPAISA_ENCRYPTION_KEY=your_encryption_key

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Trading Config
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_SIGNAL_SCORE=8
```

### Frontend .env

```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## Deployment

### Railway.app (Recommended - Free)

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

Add environment variables in Railway dashboard.

### Render.com

1. Connect GitHub repo
2. Create Web Service
3. Backend:
   - Build: `cd backend && pip install -r requirements.txt`
   - Start: `cd backend && python server.py`
4. Frontend:
   - Build: `cd frontend && npm install && npm run build`
   - Start: `npx serve -s build`

## API Endpoints

- `GET /api/health` - System health check
- `POST /api/signals/generate` - Generate trading signals
- `GET /api/signals` - Get recent signals
- `GET /api/market/regime` - Current market regime
- `GET /api/market/sectors` - Sector strength analysis
- `POST /api/backtest/run` - Run backtesting
- `GET /api/analytics/performance` - Performance metrics

## Usage

1. **Generate Signals**: Click "Generate Signals" on dashboard
2. **Receive Alerts**: Trade signals sent to Telegram
3. **Monitor Performance**: View win rate, P&L, and metrics
4. **Run Backtests**: Test strategy on historical data
5. **Start Scheduler**: Auto-generate signals every 5 minutes

## Trading Strategy

The system uses a multi-factor scoring model:

- **Price Action** (Weight: 3) - Candlestick patterns, VWAP
- **Volume** (Weight: 2) - Volume spikes, above average
- **Option Chain** (Weight: 3) - PCR, OI changes
- **Sector Strength** (Weight: 2) - Relative performance
- **Market Regime** (Weight: 2) - Trend alignment
- **Minimum Score**: 8/13 for signal generation

## Risk Management

- 1% risk per trade (configurable)
- Maximum 3 concurrent trades
- Stop loss on every trade
- 1:1.5 and 1:2 risk-reward targets
- Position sizing based on risk tolerance

## Market Hours

- **Active**: Monday-Friday, 9:15 AM - 3:30 PM IST
- **Scheduler**: Runs every 5 minutes during market hours
- **Off-hours**: No signal generation

## Screenshots

Dashboard includes:
- Live signals table
- Market regime indicator
- Sector strength heatmap
- Performance metrics
- Backtesting interface
- System status monitor

## Support

For issues or questions, check:
- Backend logs: `/var/log/supervisor/backend.err.log`
- API health: `http://localhost:8001/api/health`
- MongoDB status: `mongod --version`

## License

MIT

## Disclaimer

This is an algorithmic trading system. Use at your own risk. Past performance does not guarantee future results. Always test thoroughly before live trading.
