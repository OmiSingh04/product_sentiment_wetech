# Sentiment Analysis on Product Feedbacks

This project performs **sentiment analysis on product reviews**, extracting meaning from customer reviews.

## Project Structure

The project consists of:

- **Frontend**  
  User interface for submitting reviews and viewing sentiment results.

- **Backend**  
  Handles API requests, database operations, and sentiment analysis logic.

- **MySQL Queries**  
  SQL scripts used to construct the database tables.

## Prerequisites

Before running the project, have the following configurations inplace.

### 0. Dependencies 
The relevant dependencies from pip, which can be seen in the backend/main.py file.

### 1. Environment Variables

Create a `.env` file in the backend directory containing your MySQL credentials:

```env
DB_HOST=your_host
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```

### 2. AWS Configuration

AWS must be configured locally for `boto3` to work. Run `aws configure` in your terminal.
