# Scan-Quest
Web application for organizing quests based on scanning QR-codes

### Backend
#### Install
```sh
pip install poetry==1.8.3
poetry --directory=backend install
pre-commit install
```

#### Run
```sh
docker compose up -d --wait
```

### Frontend
```sh
cd frontend
```

#### Run (dev-mode)
```sh
npm run develop
```

#### Build
```sh
npm run build
```

Build output folder is `frontend/public` (gatsby can't change it)

It's probably worth it to shut down running dev-mode frontend and delete `frontend/public` before build, since gatsby uses this folder for dev-mode as well (why?)
