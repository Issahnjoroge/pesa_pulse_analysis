# Pesa Pulse API Analysis

## Project Overview

Pesa Pulse is a customer data analysis project that retrieves customer records from the JSONPlaceholder API, explores nested data structures, and analyses customer locations and email domain endings using Python.

## Data Source
- API https://jsonplaceholder.typicode.com/users
- HTTP method: GET
- Records retrieved: 10 customers

## Tools and Libraries
- Python
- Requests — API requests and error handling
- Pandas — data processing and verification
- Matplotlib — data visualisation

## Analysis Performe
1. Retrieved customer data from the API with a timeout.
2. Explored the nested customer record structure and data types.
3. Extracted customer details, including names, email addresses, cities, postal codes, coordinates, companies, and websites.
4. Identified unique cities using a set.
5. Counted customers per city and email domain ending using dictionaries.
6. Converted the extracted data into a pandas DataFrame.
7. Verified manual counts against pandas counts.
8. Exported CSV files and generated charts.

## Key Findings

- Customers retrieved was 10
- Unique cities are 10
- Each customer in this dataset belongs to a different city.
- The biz email ending was the most common, appearing 3 times.
- The manual city and emailmdomain counts matched the pandas results.



## Output Files
The output folder contains:

- customers.csv wwwhich extracted customer records.
- city_counts.csv which customer counts by city, sorted by count and city name.
- customer_distribution.png where there is customer distribution visualisation.
- email_domain_distribution.png with  email domain distribution visualisation.

## How to Run

1. Install the required packages

2. Run the analysis


## Limitations

The API provides a small sample of 10 customers. The results describe this sample and should not be treated as representative of a real financial institution's customer base.