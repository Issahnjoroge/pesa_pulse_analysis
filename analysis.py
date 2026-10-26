"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:        #try attempst the code
        response = requests.get(url, timeout=10)     #asks for data for a specific time
        response.raise_for_status ()
        customers = response.json ()
        return customers


    except ValueError:
        print("The API returned invalid JSON.")
        return[]

    
    except requests.exceptions.RequestException as error:   #it try fails then...
        print(f"Could not reach the API: {error}")
        return []

   

def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items():
        spacing = " " * indent
        print(f"{spacing}{key}: {type(value).__name__}")

    if isinstance(value, dict):
        explore(value, indent + 2)
    


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []
    for customer in customers:
        row = {
            "customer_id": customer["id"],
            "name": customer["name"],
            "username": customer["username"],
            "email": customer["email"],
            "email_domain": customer["email"].split(".")[-1],
            "phone": customer["phone"],
            "city": customer["address"]["city"],
            "zipcode": customer["address"]["zipcode"],
            "latitude": float(customer["address"]["geo"]["lat"]),
            "longitude": float(customer["address"]["geo"]["lng"]),
            "company": customer["company"]["name"],
            "website": customer["website"]
        }
        rows.append(row)

    return rows


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    cities = set()

    for customer in customers:
        city = customer["address"]["city"]
        cities.add(city)

    return cities


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}

    for customer in customers:
        city = customer["address"]["city"]

        if city in counts:
           counts[city] += 1
        else:
            counts[city] = 1

    return counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    domains = {}

    for customer in customers:
        email_domain = customer["email"].split(".")[-1]

        if email_domain in domains:
            domains[email_domain] += 1
        else:
            domains[email_domain] = 1

    return domains


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    return df


def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    
    
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.title("Customer Distribution")
    plt.xlabel("City" or "Email Domain")
    plt.ylabel("Number of Customers")
    plt.yticks(range(0, max(values) + 2))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path)
    plt.close()



def export_csvs(df: pd.DataFrame, counts: dict[str, int]) -> None:
    """write an save thhe customer data and sorted city counts to CSV files."""
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_dir / "customers.csv", index=False)
    city_df = pd.DataFrame(
        list(counts.items()),
        columns=["city", "customer_count"]
    )
    city_df = city_df.sort_values(
        by=["customer_count", "city"],
        ascending=[False, True]
    )

    city_df.to_csv(output_dir / "city_counts.csv", index=False)


if __name__ == "__main__":
    # TODO: run each step and print a short findings summary
    customers = get_customers()

    if not customers:
        print("No customer data available.")

    else:
        print("Structure of the first record:")
        explore(customers[0])
        print()

        rows = extract_attributes(customers)
        cities = unique_cities(customers)
        counts = city_counts(customers)
        domain_counts = email_domain_counts(customers)

        print("Unique cities:", len(cities), "| Customers:", len(customers))

        if len(cities) == len(customers):
            print("Every customers is in a different city.")
        else:
            print("Some of the customers share a city they live in.")
        print()

        print("City counts (most to least common):")
        for city, n in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            print(f" {city}: {n}")
        print()

        print("Email domain counts (most to least common):")
        for tld, n in domain_counts.items():
            print(f"  {tld}: {n}")
        print()


        df = to_dataframe(rows)

        print("DataFrame shape:", df.shape)
        print("DataFrame data types: ")
        print(df.dtypes)
        print()


        pandas_city_counts = df["city"].value_counts().to_dict()
        pandas_domain_counts = df["email_domain"].value_counts().to_dict()

        print("pandas matches city counts: ", pandas_city_counts == counts)
        print("pandas matches domain counts: ", pandas_domain_counts == domain_counts)
        print()


        export_csvs(df, counts)

        chart_path = Path("output/customer_distribution.png")
        plot_distribution(counts, chart_path)
        plot_distribution(domain_counts,
        Path("output/email_domain_distribution.png")
)

        top_city, top_n = next(iter(counts.items()))
        print("Customers retrieved:", len(customers))
        print("Unique cities:" ,len(cities))
        print(f"Most common city:{top_city} ({top_n})")
        print("Email domains:", domain_counts)
        print("Chart saved to:", chart_path)
