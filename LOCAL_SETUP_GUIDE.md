# RUN F&O TRADING SYSTEM LOCALLY - COMPLETE GUIDE

## Prerequisites

### 1. Install Required Software

**Install Python 3.11+**
- Windows: https://www.python.org/downloads/
- Mac: `brew install python@3.11`
- Linux: `sudo apt install python3.11 python3.11-venv`

**Install Node.js 18+**
- Download: https://nodejs.org/
- Install LTS version

**Install MongoDB**
- Download: https://www.mongodb.com/try/download/community
- OR use MongoDB Atlas (cloud, free): https://www.mongodb.com/cloud/atlas

**Install Git**
- Download: https://git-scm.com/downloads

---

## STEP 1: Get Code from GitHub

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

---

## STEP 2: Setup Backend

```bash
# Go to backend folder
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Edit .env file:

```bash
# Open .env in text editor
# Windows: notepad .env
# Mac: open -e .env
# Linux: nano .env
```

Make sure these are set:

```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="trading_system"
CORS_ORIGINS="*"

# Your 5paisa credentials (already configured)
FIVEPAISA_APP_NAME="5P52138530"
FIVEPAISA_APP_SOURCE="22659"
FIVEPAISA_USER_ID="nYKklT5m4il"
FIVEPAISA_USER_PASSWORD="oZX2ZBuZXMB"
FIVEPAISA_USER_KEY="OYKtwfVHzl1IgvJxkIqj1VYkVQDDqChv"
FIVEPAISA_ENCRYPTION_KEY="odsNeWIcuJCUFoIWJaysvfc1JeKdTKmw"
FIVEPAISA_EMAIL="your_email@example.com"
FIVEPAISA_DOB="19900101"

# Telegram (already configured)
TELEGRAM_BOT_TOKEN="8612914183:AAE-km2z1FI-jaucSUXleGRvbPgJ4rT8xrc"
TELEGRAM_CHAT_ID="6904917660"

# Gmail - leave empty if not using
GMAIL_SENDER=""
GMAIL_APP_PASSWORD=""
EMAIL_RECIPIENTS=""

# Trading config
RISK_PER_TRADE=0.01
MAX_CONCURRENT_TRADES=3
MIN_SIGNAL_SCORE=8
```

### Start MongoDB:

**If using local MongoDB:**
```bash
# Mac:
brew services start mongodb-community

# Linux:
sudo systemctl start mongod

# Windows:
# MongoDB starts automatically after installation
```

**If using MongoDB Atlas:**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
4. Update `MONGO_URL` in .env

### Run Backend:

```bash
# Make sure you're in backend folder and venv is activated
python server.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

**Keep this terminal open!**

---

## STEP 3: Setup Frontend

**Open a NEW terminal window**

```bash
# Go to frontend folder (from project root)
cd frontend

# Install dependencies
npm install
# OR if you prefer yarn:
yarn install
```

### Create .env file:

```bash
# Create .env file
# Windows:
echo REACT_APP_BACKEND_URL=http://localhost:8001 > .env
# Mac/Linux:
echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
```

### Run Frontend:

```bash
# Start development server
npm start
# OR
yarn start
```

Browser will automatically open at: **http://localhost:3000**

---

## STEP 4: Test It Works

### 1. Check Backend:
Open: http://localhost:8001/api/health

Should see:
```json
{
  "status": "healthy",
  "database": "connected",
  "scheduler": false
}
```

### 2. Check Frontend:
Open: http://localhost:3000

You should see the trading dashboard.

### 3. Generate Test Signal:
Click "Generate Signals" button on dashboard.

Check your Telegram - you should receive trade signal!

---

## Common Issues & Fixes

### Backend won't start:

**Error: "ModuleNotFoundError"**
```bash
# Make sure venv is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall
pip install -r requirements.txt
```

**Error: "MongoDB connection failed"**
- Check if MongoDB is running: `mongod --version`
- Start MongoDB (see commands above)
- OR use MongoDB Atlas cloud

**Error: "Port 8001 already in use"**
```bash
# Find and kill process
# Mac/Linux:
lsof -ti:8001 | xargs kill -9
# Windows:
netstat -ano | findstr :8001
taskkill /PID <PID_NUMBER> /F
```

### Frontend won't start:

**Error: "Port 3000 already in use"**
- Choose different port when prompted (Y)
- OR kill process on 3000

**Error: "Module not found"**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: "CORS error"**
- Make sure backend .env has: `CORS_ORIGINS="*"`
- Restart backend

---

## How to Stop

**Stop Backend:**
- Press `Ctrl+C` in backend terminal

**Stop Frontend:**
- Press `Ctrl+C` in frontend terminal

**Stop MongoDB (if local):**
```bash
# Mac:
brew services stop mongodb-community
# Linux:
sudo systemctl stop mongod
```

---

## File Structure

```
YOUR_REPO/
├── backend/
│   ├── server.py          # Main FastAPI app
│   ├── config.py          # Configuration
│   ├── .env               # Environment variables
│   ├── requirements.txt   # Python dependencies
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── alerts/            # Telegram/Email
│   ├── backtest/          # Backtesting engine
│   └── scheduler/         # Auto signal generation
│
├── frontend/
│   ├── package.json       # Node dependencies
│   ├── .env               # Backend URL
│   ├── public/            # Static files
│   └── src/
│       ├── App.js         # Main component
│       ├── components/    # React components
│       └── api/           # API client
│
└── README.md
```

---

## Next Steps

Once running locally:

1. **Test Signal Generation**: Click "Generate Signals"
2. **Check Telegram**: Should receive alerts
3. **Run Backtest**: Test with historical data
4. **Start Scheduler**: Auto-generate signals every 5 min
5. **Monitor Performance**: Check analytics panel

---

## Deploy for 24/7

When ready to go live, see: `/app/DEPLOYMENT_GUIDE.md`

Options:
- Emergent Deploy (easiest)
- Railway.app (free tier)
- Render.com (free tier)
- Your own VPS

---

## Need Help?

If stuck:
1. Check backend logs in terminal
2. Check browser console (F12)
3. Verify .env files are correct
4. Make sure MongoDB is running
5. Try restarting both backend and frontend

The system works - you just need to get it running on your machine!
