# FuturePath submission entry point

The SDC example repository shows a `src/main.py` application entry point.
FuturePath includes that path for clarity and reviewer convenience, while
**keeping its actual production implementation in `backend/`**.

- `src/main.py`: imports and exposes `backend.app:app` (same FastAPI app).
- `backend/app.py`: app setup, middleware and feature routers.
- `backend/routes/`: independent APIs for CVs, careers, Signals and pathways.
- `frontend/mockup_source/`: editable V2 interface.
- `runpod_worker/handler.py`: actual GPU inference worker.

Start locally with `python src/main.py` or with
`python -m uvicorn src.main:app --host 0.0.0.0 --port 5000`.

**Do not copy the organizer's placeholder echo app or move the existing
backend modules**: that would risk breaking the tested Replit/RunPod integration.
