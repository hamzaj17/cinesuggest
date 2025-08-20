# 🎬 CineSuggest - Movie Recommendation System

CineSuggest is an intelligent **movie recommendation system** that combines **content-based filtering**, **collaborative filtering** and **hybrid approach** to provide personalized movie suggestions.  
It uses Python (FastAPI backend) and can be tested using **Postman**.

---

## 📂 Project Structure

<pre>
  cinesuggest/
│── Model Development/
│   │── data/       # All datasets (movies, ratings, etc.)
│   │── models/     # Saved/trained models
│   │── src/        # All Python source code files
│   │── fastapi_app.py  # FastAPI app for API testing
│── README.md

</pre>

---

## ⚙️ Libraries Used
Make sure you have Python 3.8+ installed. Install the required libraries:
```
pip install fastapi pandas scikit-learn scikit-surprise joblib
```
Other built-in libraries used:

- pickle (Python built-in, no need to install)
- ast (Python built-in, no need to install)

---

## 🚀 How to Run

Follow this order to run the project correctly:

### 1️⃣ Content-Based Filtering

Run the script to prepare the content-based recommendation model:
```
python src/model_cb.py
```

### 2️⃣ Preprocess Data for CF

Cleans and prepares the dataset for collaborative filtering:
```
python src/train_cf.py
```

### 3️⃣ Train Collaborative Filtering Model

Trains the CF model and saves it:
```
python src/train_cf.py
```

### 4️⃣ Generate CF Recommendations

Generates recommendations using collaborative filtering:
```
python src/recommend_cf.py
```

### 5️⃣ Hybrid Model

Combines both CBF + CF to make hybrid recommendations:
```
python -m src.hybrid
```

### 6️⃣ Main Script

Runs the complete recommendation pipeline:
```
python -m src.main  
```

---

## 🌐 Run FastAPI Server

Finally, use FastAPI to serve recommendations:
```
uvicorn fastapi_app:app --reload
```
This will start the server at:
```
http://127.0.0.1:8000
```
Check the interactive API docs at:
```
http://127.0.0.1:8000/docs
```

---

## 📬 Testing with Postman

- Open Postman.
- Send a POST request to:
```
http://127.0.0.1:8000/recommend?user_id=1
```
You will get movie recommendations generated through Collaborative Filtering.

---

## ✅ Notes

- Ensure that the data folder contains the required datasets before running.

- Trained models will be saved in the models folder automatically.

- Run scripts in order, then use FastAPI + Postman to test movie suggestions.

---

## 📥 Dataset Access

For access to the datasets, please drop an email:

📧 [hamzabjaved04@gmail.com](mailto:hamzabjaved04@gmail.com)

