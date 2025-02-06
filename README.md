# Interviewer Scheduler API

This is a DRF API that allows candidates and interviewers to schedule available time slots and check overlapping availability.
## Features
- Register availability for **candidates** and **interviewers**.
- Check **overlapping time slots**.
- Retrieve stored availability.

## Installation Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Athulraj72/interview_scheduler
   
## Create  a Virtual Environment
    ```bash
    python -m venv venv 
    source venv/bin/activate

## Install Dependencies
    ```bash
    pip install -r requirements.txt

## Run Migrations
    ```bash
    python manage.py migrate

## Start the Server
    ```bash
    python manage.py runserver

## Testing API Using Postman
- Open Postman.
- Choose "New Request".
    
### **🔹  Add Candidate Availability**
To register **candidate availability**, send a **POST** request:

- **Method:** `POST`
- **URL:** http://127.0.0.1:8000/api/scheduler/
- **Headers:**  
In the **Headers** section of Postman, set:
- Key: Content-Type   Value: application/json
  - **Body (JSON):**
      ```json
      {
      "user_id": "100",
      "user_type": "CANDIDATE",
      "start_time": "2024-02-06T10:00:00Z",
      "end_time": "2024-02-06T14:00:00Z"
      }
-Click Send.

### **🔹  Add Interviewer Availability**
- **Method:** `POST`
- **URL:** http://127.0.0.1:8000/api/scheduler/
  - **Headers:**  
  In the **Headers** section of Postman, set:
    - Key: Content-Type   Value: application/json
      - **Body (JSON):**
        ```json
         {
          "user_id": "200",
          "user_type": "INTERVIEWER",
          "start_time": "2024-02-06T11:00:00Z",
          "end_time": "2024-02-06T15:00:00Z"
        }

### **🔹  Check Overlapping Time Slots**
- Method: POST
- - **Headers:**  
  In the **Headers** section of Postman, set:
    - Key: Content-Type   Value: application/json
- **URL:** http://127.0.0.1:8000/api/scheduler/check_overlap/
  - **Body (JSON):**
  ```json
    {
    "candidate_id": "100",
    "interviewer_id": "200",
    "date": "2024-02-06"
    }
### **🔹  Expected Response**
    ```json
    {
    "overlapping_slots": [
        {
            "date": "2024-02-06",
            "start_time": "11:00",
            "end_time": "12:00"
        },
        {
            "date": "2024-02-06",
            "start_time": "12:00",
            "end_time": "13:00"
        },
        {
            "date": "2024-02-06",
            "start_time": "13:00",
            "end_time": "14:00"
        }
    ],
    "availability_summary": {
        "candidate": [
            {
                "date": "2024-02-06",
                "start_time": "10:00",
                "end_time": "14:00"
            }
        ],
        "interviewer": [
            {
                "date": "2024-02-06",
                "start_time": "11:00",
                "end_time": "15:00"
            }
        ]
    }
    }

###  Assumptions made:
-No user authentication is implemented.Assume that users are correctly entering their IDs.If a candidate and interviewer are both available within a time range, 
the API generates overlapping 1-hour slots. The API expects JSON-formatted requests with Content-Type: application/json.
If this header is missing, the request may not be parsed correctly.
All time slots are assumed to be in UTC format. And I assume that there is one candidate and one interviewer involved per meeting.

### Better solutions
-instead of overlapping approach,interviewers define their available time slots and candidates can select the time slot which is suitable for them.This will help to eliminate need for checking overlaps in database and making sytem more efficient and removing the need for hr invention.

### Improvement in my solution
- Add authentication & user roles.
- Make arrangements for bulk Upload & Auto-Scheduling
