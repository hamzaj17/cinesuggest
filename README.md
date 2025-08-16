# 🎬 CineSuggest - Movie Recommendation System

CineSuggest is an intelligent movie recommendation system that combines Content-Based Filtering (CBF), Collaborative Filtering (CF), and Hybrid approaches to provide personalized movie suggestions.

---

## Project Structure
<pre>
cinesuggest/
│── Model Development/
│   │── fastapi_app.py
│   │── data/
│   │   └── (datasets here)
│   │── models/
│   │   └── (trained models here)
│   │── src/
│       └── (all code files here)
│── README.md
</pre>

---

## 📦 Required Libraries

Make sure you have the following Python libraries installed:

```
pip install fastapi pandas scikit-learn scikit-surprise joblib
```

Additional built-in libraries used:

- pickle
- ast

---

## 🚀 How to Run the Project

Follow these steps in order to run the system:

**1)Content-Based Filtering Model**
<pre>python src/model_cb.py</pre>

**2)Preprocess Collaborative Filtering Data**
<pre>python src/preprocess_cf.py</pre>

**3)Train Collaborative Filtering Model**
<pre>python src/train_cf.py</pre>

**4)Generate Recommendations with Collaborative Filtering**
<pre>python src/recommend_cf.py</pre>

**5)Hybrid Model (Combining CB + CF)**
<pre>python -m src.hybrid</pre>

**6)Run the Main Script**
<pre>python -m src.main</pre>

---

## 🌐 Run FastAPI

After running the above steps, start the FastAPI server:
```
uvicorn fastapi_app:app --reload
```
This will start the backend at:
<pre>http://127.0.0.1:8000</pre>

Check the interactive API docs at:
<pre>http://127.0.0.1:8000/docs</pre>

---

## 📬 Testing with Postman

- Open Postman.
- Use POST requests to send movie/user data to FastAPI endpoints.
- You will get movie recommendations generated through Collaborative Filtering.

Send a Get Request to:
```
http://127.0.0.1:8000/recommend?user_id=1
```

---

- Run scripts in order, then use FastAPI + Postman to test movie suggestions.
- For access to the datasets, please drop an email:

📧 [hamzabjaved04@gmail.com](mailto:hamzabjaved04@gmail.com)

---

## 🤝 Contributing

Feel free to fork this project, improve it, and submit pull requests 🚀
