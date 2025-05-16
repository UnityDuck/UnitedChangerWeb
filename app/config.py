import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    UPLOAD_FOLDER = 'static/uploads'
    TRADERMADE_API_KEY = 'eGCvr06hXSw0oinclXKs'
    TRADERMADE_API_URL = 'https://marketdata.tradermade.com/api/v1/timeseries'
