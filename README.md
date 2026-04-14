# 📦 IT Inventory Management System

A professional, enterprise-level IT Inventory Management System built with Django. This system allows businesses to efficiently manage their warehouse stock, categorize products, and track product transfers to various branch outlets in real-time.

## ✨ Key Features

* **🎛️ Modern Dashboard UI:** Beautiful and responsive admin interface powered by the Jazzmin theme.
* **⚠️ Dynamic Low-Stock Alerts:** Color-coded badges to easily identify stock levels:
  * 🔴 **Red:** Extreme Low Stock (5 or below)
  * 🟠 **Orange:** Reorder Soon (6 to 10)
  * 🟢 **Green:** Adequate Stock (Above 10)
* **📊 One-Click Reporting:** Export Product lists and Transfer History directly to CSV/Excel formats for data analysis.
* **🔄 Seamless Transfers:** Easily track products sent from the main warehouse to specific outlets.
* **📜 Immutable Transfer History:** Read-only tracking of all historical transfer records with Challan references.
* **📋 Smart Form Layouts:** Enterprise-style data entry forms using organized fieldsets and descriptions.
* **🔤 Custom Admin Sorting:** Alphabetically sorted and logically grouped navigation menus.

## 🛠️ Technologies Used

* **Backend:** Python, Django
* **Database:** SQLite (Default)
* **Frontend:** Django Admin Templates, HTML, CSS
* **UI Theme:** Django-Jazzmin

## 🚀 How to Run Locally


Extract the ZIP file or Clone the repository.

Open terminal in the project folder.

Install all requirements using: pip install -r requirements.txt

Run the project: python manage.py runserver

Access the Dashboard: http://127.0.0.1:8000/

Admin Panel: http://127.0.0.1:8000/admin/

Admin password :
Username: admin
Password: admin

If you want to run this project on your local machine, follow these simple steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/expartrasel/IT-Inventory-System.git](https://github.com/expartrasel/IT-Inventory-System.git)
   cd IT-Inventory-System
