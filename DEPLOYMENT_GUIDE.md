# HOW TO RUN YOUR F&O TRADING SYSTEM LOCALLY

## STEP 1: Push Code to GitHub

Run these commands on Emergent:

```bash
cd /app

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "F&O Trading System - Initial commit"

# Add your GitHub repo (replace with YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push
git push -u origin main
```

Or use the **"Save to GitHub"** button in the Emergent chat.

---

## STEP 2: Clone and Run on Your Local Machine

### Prerequisites:
- Python 3.11+
- Node.js 18+
- MongoDB installed locally OR use MongoDB Atlas (free cloud)

### Backend Setup:

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# Backend
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup MongoDB
# Option A: Install MongoDB locally
# Download from: https://www.mongodb.com/try/download/community

# Option B: Use MongoDB Atlas (cloud - easier)
# 1. Go to mongodb.com/cloud/atlas
# 2. Create free cluster
# 3. Get connection string
# 4. Update MONGO_URL in .env

# Edit .env file with your actual values
nano .env  # or use any text editor

# Update these in .env:
MONGO_URL="mongodb://localhost:27017"  # or your Atlas URL
TELEGRAM_BOT_TOKEN="8612914183:AAE-km2z1FI-jaucSUXleGRvbPgJ4rT8xrc"
TELEGRAM_CHAT_ID="6904917660"
# ... all your 5paisa credentials ...

# Run backend
python server.py
```

Backend will run on: `http://localhost:8001`

### Frontend Setup:

```bash
# Open NEW terminal, go to frontend folder
cd frontend

# Install dependencies
npm install
# or
yarn install

# Create .env file
echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env

# Run frontend
npm start
# or
yarn start
```

Frontend will open in browser at: `http://localhost:3000`

---

## STEP 3: Deploy for 24/7 (Choose One)

### Option A: Deploy on Emergent (Easiest)
1. Click "Deploy" in Emergent chat
2. Costs 50 credits/month
3. Automatic 24/7 hosting
4. Done!

### Option B: Railway.app (Free Tier Available)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway init
railway up
```

Add environment variables in Railway dashboard.

### Option C: Render.com (Free Tier)

1. Go to render.com
2. New → Web Service
3. Connect your GitHub repo
4. Backend:
   - Build: `cd backend && pip install -r requirements.txt`
   - Start: `cd backend && python server.py`
5. Frontend:
   - Build: `cd frontend && npm install && npm run build`
   - Start: `serve -s build`

Add environment variables in Render dashboard.

---

## CURRENT STATUS - HONEST ANSWER

### What's Actually Working:
✅ Backend API - all endpoints functional
✅ Frontend Dashboard - fully working UI
✅ Database - MongoDB connected
✅ Telegram - Bot configured, alerts working
✅ Signal Generation - Logic implemented
✅ Backtesting - Engine ready

### What's NOT Working:
❌ **5paisa Real Data** - Using MOCK data because:
   - py5paisa library has authentication issues
   - Your credentials are configured but library connection fails
   - Need to either:
     a. Fix py5paisa integration (requires debugging library)
     b. Use 5paisa REST API directly (bypass library)
     c. Keep using mock data for testing

❌ **24/7 Uptime** - Preview environment is temporary
   - Need to deploy (see Step 3 above)

### What You Can Do RIGHT NOW:

1. **Test with Mock Data** (Working)
   - Generate signals
   - Get Telegram alerts
   - Test backtesting
   - Learn the system

2. **Run Locally** (Follow Step 2)
   - Full control
   - No dependency on Emergent
   - Free

3. **Deploy for 24/7** (Follow Step 3)
   - Choose deployment platform
   - Set environment variables
   - Go live

---

## To Get REAL 5paisa Data

The py5paisa library has issues. Two options:

### Option 1: Use 5paisa REST API Directly
I can rewrite the market_data.py to call 5paisa HTTP endpoints directly instead of using the broken library.

### Option 2: Try Different Broker
Use brokers with better APIs:
- Zerodha Kite (most popular in India)
- Upstox
- Angel One
- Finvasia

All have better Python libraries and documentation.

---

## Bottom Line

The system IS working - just using mock data for market prices instead of real 5paisa data. Everything else (alerts, signals, backtesting, dashboard) works.

**You can:**
1. Run it locally right now (Step 2)
2. Deploy it for 24/7 (Step 3)
3. Either fix 5paisa OR switch broker OR keep testing with mock data

**Your code is yours** - not locked to Emergent. Take it and run anywhere.
