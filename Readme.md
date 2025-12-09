# 🚗 RentCar.uz Backend API

Bu repository **rentcar.uz** loyihasining backend qismi uchun yozilgan **REST API** ni o'z ichiga oladi. Backend **Python / Django REST Framework (DRF)** asosida ishlab chiqilgan va avtomobil ijarasi (rent) jarayonlarini to‘liq qamrab oladi.

---

## 📌 Texnologiyalar

* Python 3.10+
* Django
* Django REST Framework
* drf-spectacular (Swagger / OpenAPI)
* PostgreSQL
* JWT Authentication (SimpleJWT)
* django-filter

---

## 🔐 Authentication

Autentifikatsiya **telefon raqam + SMS code** orqali amalga oshiriladi.

### 1️⃣ SMS kod yuborish

**POST** `/api/v1/auth/send-code`

```json
{
  "phone": "+998901001010"
}
```

**Response**

```json
{
  "detail": "SMS yuborildi!"
}
```

---

### 2️⃣ SMS kodni tasdiqlash (Login)

**POST** `/api/v1/auth/verify-code`

```json
{
  "phone": "+998901001010",
  "code": 123456
}
```

**Response**

```json
{
  "message": "OK.",
  "data": {
    "access_token": "jwt_access_token",
    "refresh_token": "jwt_refresh_token",
    "user": {
      "id": "uuid",
      "phone": "901001010"
    }
  }
}
```

---

## 👤 User Profile

### Foydalanuvchi profilini to‘ldirish

**POST** `/api/v1/auth/register`

🔒 **Authorization required**

```json
{
  "first_name": "Ali",
  "last_name": "Valiyev",
  "passport_series": "AA1234567"
}
```

---

## 📰 News

### Yangiliklar ro‘yxati

**GET** `/api/v1/news`

### Yangilik qo‘shish (Admin)

**POST** `/api/v1/news`

---

## 🏷 Brand & Category

### Brandlar ro‘yxati

**GET** `/api/v1/brands`

### Brand qo‘shish (Admin)

**POST** `/api/v1/brands`

---

### Categoriyalar ro‘yxati

**GET** `/api/v1/categories`

### Category qo‘shish (Admin)

**POST** `/api/v1/categories`

---

## 🚘 Cars

### Mashinalar ro‘yxati

**GET** `/api/v1/cars`

🔍 Filter & Search qo‘llab-quvvatlanadi:

* brand
* category
* price
* search (name, brand)

---

### Mashina detail

**GET** `/api/v1/cars/{uuid}`

---

### Mashina yaratish (Admin)

**POST** `/api/v1/cars`

---

### Mashina yangilash (Admin)

**PUT / PATCH** `/api/v1/cars/{uuid}`

---

### Mashina o‘chirish (Admin)

**DELETE** `/api/v1/cars/{uuid}`

---

## 📆 Rentals (Ijara)

### Mashina ijaraga olish

**POST** `/api/v1/user/rentals`

🔒 **Authorization required**

```json
{
  "car": "uuid",
  "pick_up_data_time": "2025-01-01T10:00:00",
  "drop_of_data_time": "2025-01-05T10:00:00"
}
```

---

### Foydalanuvchi ijaralari

**GET** `/api/v1/user/rentals`

---

### Ijara tarixi

**GET** `/api/v1/rentals/history`

---

## 🔐 Permissions

| Role  | Huquqlar                              |
| ----- | ------------------------------------- |
| Guest | GET endpointlar                       |
| User  | Rent, Profile                         |
| Admin | CRUD (Cars, Brands, Categories, News) |

---

## 📊 API Documentation (Swagger)

Swagger avtomatik generatsiya qilingan:

👉 `http://127.0.0.1:8000/ru/`

---

## ⚙️ Run project

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📁 Project Structure (Short)

```text
apps/
 ├── models/
 ├── serializers/
 ├── views/
 ├── filters/
 ├── permissions/
 └── urls.py
```

---

## 👨‍💻 Author

**RentCar.uz Backend API**

Agar savollar yoki takliflar bo‘lsa — issue ochishingiz mumkin 👍
