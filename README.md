# Interview Bot — Full (Feature-Complete)

## Local
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:api --reload --port 8000

# Frontend
cd ../frontend
cp .env.example .env.local
# Set BACKEND_URL=http://localhost:8000
npm install
npm run dev

## Quick API smoke tests
# health
curl http://localhost:8000/health

# interview
curl -X POST http://localhost:8000/interview/start -H "Content-Type: application/json" \
  -d '{"industry":"software","personas":["hr","tech","manager"],"difficulty":"easy","stressLevel":1}'

# analyze text
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" \
  -d '{"transcript":"I led the team and shipped with 40% faster cycle times.","durationSeconds":40}'

# culture fit
curl -X POST http://localhost:8000/culturefit/score -H "Content-Type: application/json" \
  -d '{"transcript":"I value ownership, customer focus, and iterating quickly."}'

# audio
curl -X POST http://localhost:8000/audio/analyze -F "file=@sample.wav"

# image
curl -X POST http://localhost:8000/image/analyze -F "file=@frame.jpg"

# negotiation
curl -X POST http://localhost:8000/negotiation/start -H "Content-Type: application/json" \
  -d '{"role":"Software Engineer","candidateAnchor":24.0}'
