# 🌤️ Weather Notification System

A smart assistant that automatically checks the weather in Tokyo and sends you notifications wherever it's convenient: to **Discord**, **LINE**, or **Email**.

Set it up once — and the weather comes to your messenger by itself.

## 📁 Project structure

notify/
├── discord/
│   ├── .env
│   ├── api_req.py
│   └── notify.py
├── gmail/
│   ├── .env
│   ├── api_req.py
│   └── notify.py
├── line/
│   ├── .env
│   ├── api_req.py
│   └── notify.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

## 🚀 Quick Start Guide

```bash
# Clone the repository
git clone https://github.com/VersaLog/notify.git
cd notify

# Install dependencies
pip install -r requirements.txt