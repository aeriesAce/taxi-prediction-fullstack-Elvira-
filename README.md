# taxi-prediction-fullstack-Elvira-opa24
## A school project where we will create an ML-model to predict taxi prices

>[!IMPORTANT]
>**The dataset is fetched from [kaggle](https://www.kaggle.com/datasets/denkuznetz/taxi-price-prediction)**

>[!NOTE]
>***This is created for educational purpose only!***

<ins>Purpose</ins>:\
This project aims to implement a backend and frontend to solve a real-world problem.
The backend and frontend communicate through an API layer to keep the components decoupled from each other.
The application will serve a machine learning model to make relevant predictions.
<details>
<summary><ins>Situation</ins></summary>
Company Overview and Project Context
"Resekollen AB has previously developed applications for visualizing and planning trips using public transportation. They now aim to expand into a related area: taxi rides. The company wants to predict taxi fares and has hired you as an intern (LIA student) to assist with this. With your skills in machine learning, OOP, APIs, backend, frontend, and other relevant areas, the project is expected to proceed smoothly.

A former machine learning engineer (MLE), together with the product owner (PO), has drafted the architecture and built a basic code structure that you will continue developing. Unfortunately, the MLE was headhunted by another company and decided to leave, but before departing, they also created the foundational code structure that you will take over."
</details>

>[!NOTE]
>This is temporary, will be fixed in upcoming update
## How to run:
| Information  | Command |
| ------------- | ------------- |
| First create an virtual enviroment | ```uv venv```|
| Activate it in your terminal  | ```source .venv/Scripts/activate``` or ```source venv/bin/activate ```  |
| Install the requirements  | ```uv pip install -r requirements.txt```  |
| In one terminal access the backend folder | ```cd src/taxipred/backend```  |
| Run uvicorn from the backend folder  | ```uvicorn api:app --reload ```  |
| In one terminal access the frontend folder   | ```cd src/taxipred/frontend```  |
| Access the localhost `127.0.0.1:8000`   |  Access the link in the terminal  |
| In the window add docs at the end of the address  |  `127.0.0.1:8000/docs`  |
| Run streamlit from the frontend folder  | ```streamlit run dashboard.py ```  |



Future implementaions:
- [ ]Connect to Google Maps
    - User can write in addresses
    - They will get recomendations based on locations
