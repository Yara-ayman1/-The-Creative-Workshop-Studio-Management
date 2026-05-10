# 🚀 The Creative Workshop & Studio Management System

## 1️⃣ سحب المشروع (Clone)

افتح الـ Terminal ثم نفذ الأوامر التالية:

```powershell
git clone https://github.com/Yara-ayman1/-The-Creative-Workshop-Studio-Management.git
cd -The-Creative-Workshop-Studio-Management
cd Workshop_Studio
```

---

## 2️⃣ إنشاء البيئة الافتراضية (Virtual Environment)

```powershell
python -m venv venv
```

يمكنك تغيير اسم `venv` لأي اسم آخر عادي.

---

## 3️⃣ تفعيل البيئة الافتراضية

```powershell
.\venv\Scripts\activate
```

إذا ظهر `(venv)` في الـ Terminal فهذا يعني أن التفعيل تم بنجاح.

---

## 4️⃣ تثبيت المكتبات المطلوبة

```powershell
pip install -r requirements.txt
```

يقوم هذا الأمر بتثبيت جميع الـ Packages المطلوبة للمشروع.

---

## 5️⃣ إعداد قاعدة البيانات (SQL Server)

### أولاً:
افتح الـ CMD واكتب:

```powershell
hostname
```

سيظهر لك اسم جهازك (Hostname).

---

### ثانياً:
أضف بياناتك داخل ملف `settings.py` بالشكل التالي:

```python
DATABASES_CONFIG = {
    'DEVICE_NAME': {
        'NAME': 'DATABASE_NAME',
        'HOST': 'DEVICE_NAME',
    },
}
```

قم باستبدال:

- `DEVICE_NAME` → باسم جهازك
- `DATABASE_NAME` → باسم قاعدة البيانات الخاصة بك

---

## 6️⃣ تشغيل السيرفر

```powershell
python manage.py runserver
```

بعد التشغيل افتح الرابط التالي في المتصفح:

```text
http://127.0.0.1:8000/
```

---

# ⚠️ ملاحظات مهمة

- ممنوع استخدام Django ORM أو Models.
- أي تعامل مع قاعدة البيانات يكون باستخدام Raw SQL فقط.
- إذا قمتِ بتعديل في الـ Database يجب إرسال الـ SQL Script لباقي الفريق.
- عند تثبيت أي مكتبة جديدة يجب تحديث ملف `requirements.txt` باستخدام:

```powershell
pip freeze > requirements.txt
```
