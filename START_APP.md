# 🚀 Quick Start - Run the Full Application

## Simple 2-Step Setup

### 1. Start Backend (Terminal 1)

```bash
cd /Users/jasperlinke/Python-Projects/real-estate-deal-evaluator
source venv/bin/activate
python -m uvicorn backend.main:app --reload
```

✅ Backend running at: **http://localhost:8000**
📚 API docs: **http://localhost:8000/docs**

### 2. Start Frontend (Terminal 2)

```bash
cd /Users/jasperlinke/Python-Projects/real-estate-deal-evaluator/frontend
npm start
```

✅ Frontend running at: **http://localhost:3000**

## Access the Application

Open your browser to: **http://localhost:3000**

## First Time Setup

If you haven't installed dependencies yet:

**Backend:**
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API keys
```

**Frontend:**
```bash
cd frontend
npm install
```

## Usage

1. **Enter property details** in the left panel form
2. **Click "Analyze Property"**
3. **View results**: 
   - Middle panel: Charts and metrics
   - Right panel: Verdicts and strategy fits
4. **Chat with AI** for insights and questions

## Need Help?

- See **SETUP.md** for detailed setup instructions
- See **README.md** for comprehensive documentation
- API documentation: http://localhost:8000/docs

---

**Enjoy analyzing Paris real estate investments! 🏠📊**
