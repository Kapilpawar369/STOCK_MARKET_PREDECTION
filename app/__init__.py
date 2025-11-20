# StockPulse/
# │
# ├── app/
# │   ├── main.py
# │   ├── __init__.py
# │
# │   ├── api/                       # All API routers grouped here
# │   │    ├── v1/
# │   │    │    ├── auth.py
# │   │    │    ├── stocks.py
# │   │    │    ├── wishlist.py
# │   │    │    ├── payments.py
# │   │    │    ├── notifications.py
# │   │    │    └── users.py
# │   │    └── deps.py               # Dependencies (get_db, Auth checks etc.)
# │
# │   ├── core/                      # Core settings of the project
# │   │    ├── config.py             # Settings, Env
# │   │    ├── database.py           # DB sessions
# │   │    ├── security.py           # Hashing, JWT, OAuth
# │   │    ├── scheduler.py          # APScheduler / Celery beat jobs
# │   │    ├── throttling.py         # Rate limiting
# │   │    ├── exceptions.py         # Global custom exceptions
# │   │    └── startup.py            # Startup events, init scripts
# │
# │   ├── models/                    # All SQLAlchemy models at one place
# │   │    ├── user.py
# │   │    ├── stock.py
# │   │    ├── wishlist.py
# │   │    ├── payment.py
# │   │    └── notification.py
# │
# │   ├── schemas/                   # Pydantic schemas centralized
# │   │    ├── user.py
# │   │    ├── auth.py
# │   │    ├── stock.py
# │   │    ├── wishlist.py
# │   │    ├── payment.py
# │   │    └── notification.py
# │
# │   ├── services/                  # Business logic lives here (clean!)
# │   │    ├── user_service.py
# │   │    ├── auth_service.py
# │   │    ├── stock_service.py
# │   │    ├── wishlist_service.py
# │   │    ├── payment_service.py
# │   │    ├── email_service.py
# │   │    └── prediction_service.py
# │
# │   ├── ml/                        # ML related code isolated
# │   │    ├── data/
# │   │    │    ├── raw/
# │   │    │    ├── processed/
# │   │    │    └── dataset_loader.py
# │   │    ├── models/
# │   │    │    ├── trained_model.pkl
# │   │    │    └── model_builder.py
# │   │    ├── preprocessing.py
# │   │    ├── feature_engineering.py
# │   │    └── predictor.py
# │
# │   ├── jobs/                      # Background tasks + cron jobs
# │   │    ├── stock_refresh.py      # Fetch daily stock prices
# │   │    ├── daily_prediction.py   # Daily prediction generator
# │   │    ├── email_reminders.py
# │   │    └── cleanup_tasks.py
# │
# │   ├── middlewares/               # Custom FastAPI middlewares
# │   │    ├── throttling.py
# │   │    ├── logging.py
# │   │    └── request_id.py         # Assign request UUID
# │
# │   ├── utils/                     # Utilities used across app
# │   │    ├── logger.py
# │   │    ├── constants.py
# │   │    ├── helpers.py
# │   │    └── jwt_tools.py
# │
# │   ├── tests/                     # pytest tests
# │   │    ├── api/
# │   │    │    ├── test_auth.py
# │   │    │    ├── test_stocks.py
# │   │    │    ├── test_wishlist.py
# │   │    │    ├── test_payments.py
# │   │    │    └── test_notifications.py
# │   │    ├── ml/
# │   │    │    └── test_prediction.py
# │   │    └── utils/
# │   │         └── test_helpers.py
# │
# │   └── static/
# │        └── emails/
# │            └── templates/
# │
# ├── alembic/
# │   ├── versions/
# │   └── env.py
# │
# ├── .env
# ├── .gitignore
# ├── Dockerfile
# ├── docker-compose.yml
# ├── requirements.txt
# └── README.md
