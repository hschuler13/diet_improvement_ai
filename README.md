# Diet Improvement AI

Food Nutrition AI is a Python-based project that helps users create healthier diets through recipe tailoring with nutrition data through interacting with an AI assistant.

---

## Requirements

* Python 3.10+
* pip
* Virtual environment recommended

---

## Project Setup

### 1. Clone the repository, cd into 

```bash
git clone <your-repo-url>
cd diet_improvement_ai
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac / Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_api_key_here
```

---

## Running the Project

### Start Streamlit Frontend from Root Folder

```bash
streamlit run frontend/app.py
```

---

## Common Errors

### API Credit Errors

We are on a free plan with our API key, so an error may appear regarding hitting the free tier requests limit.

---

## Group
Helena Schuler, Kashvi Teli
