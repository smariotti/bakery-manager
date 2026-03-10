# 🥖 Bakery Manager

A Django web app for tracking bakery production and sales — designed for tablets and used by bakers, shapers, mixers, kitchen staff, pastry staff, and front of house.

## Features

- **Dashboard** — Today's production at a glance, plus products ready to sell
- **Production** — Create and track batches through each stage (mixing → shaping → proofing → baking → ready)
- **Inventory** — Manage products and ingredients with low-stock alerts
- **Sales** — Log sales by channel (counter, wholesale, online)
- **Admin** — Full Django admin for data management

## Quick Start (Windows 11)

```bash
# 1. Clone the repo
git clone https://github.com/smariotti/bakery-manager.git
cd bakery-manager

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create an admin user
python manage.py createsuperuser

# 6. Start the server (accessible on your local network)
python manage.py runserver 0.0.0.0:8000
```

Then open `http://<your-pc-ip>:8000` on any tablet browser.

## Project Structure

```
bakery_manager/
├── bakery_manager/     # Project settings & URLs
├── production/         # Batch tracking models/views
├── inventory/          # Products & ingredients
├── sales/              # Sales logging
└── templates/          # HTML templates (Bootstrap 5)
```

## Extending the App

Good next steps as you learn Django:

- Add Django Forms classes (`forms.py`) for better validation
- Add user authentication (login required for sales)
- Add date filtering to the sales log
- Add a recipes/formula app linking products to ingredients
- Add reporting views (daily totals, waste tracking)
