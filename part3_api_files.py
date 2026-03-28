import requests
import json
import os
from datetime import datetime


# Task 1 — File Operations (Basic Level)

print("--- TASK 1: FILE HANDLING ---")

# Step 1: Writing the initial notes
# I'm using a simple multi-line string instead of a list to keep it manual
initial_notes = """Topic 1: Variables store data. Python is dynamically typed.
Topic 2: Lists are ordered and mutable.
Topic 3: Dictionaries store key-value pairs.
Topic 4: Loops automate repetitive tasks.
Topic 5: Exception handling prevents crashes."""

# Opening file in 'w' mode for a fresh start
my_file = open("python_notes.txt", "w", encoding="utf-8")
my_file.write(initial_notes)
my_file.close()
print("Success: Initial notes written to python_notes.txt")

# Step 2: Adding my own 2 lines using append mode 'a'
extra_stuff = "\nTopic 6: API stands for Application Programming Interface.\nTopic 7: File handling is used to save data permanently."
with open("python_notes.txt", "a", encoding="utf-8") as notebook:
    notebook.write(extra_stuff)
print("Success: Added two extra topics to the file.")

# Step 3: Reading and numbering each line
print("\n--- Numbered Notes ---")
counter = 1
with open("python_notes.txt", "r", encoding="utf-8") as read_doc:
    for line in read_doc:
        # Checking if line is not empty
        if line.strip():
            print(f"{counter}. {line.strip()}")
            counter += 1
print(f"Final count: Total {counter-1} lines found.")

# Step 4: Simple Search Feature
user_query = input("\nWhich word do you want to search in the notes? ").lower()
match_found = False
with open("python_notes.txt", "r", encoding="utf-8") as search_file:
    for line in search_file:
        if user_query in line.lower():
            print(f"Found it: {line.strip()}")
            match_found = True

if not match_found:
    print(f"Oops! The keyword '{user_query}' isn't in our notes.")



# Task 2 & 4: API Functions & Error Logger

# Creating a simple logger function first so I can use it later
def write_to_log(function_name, error_name, detail):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] ERROR in {function_name}: {error_name} — {detail}\n"
    # Using 'a' mode so we don't delete previous errors
    with open("error_log.txt", "a") as log_file:
        log_file.write(log_line)

print("\n--- TASK 2: PRODUCT EXPLORER (API) ---")

# Task 2 - Step 1: Fetching 20 products safely (Task 3 Exception logic included)
api_url = "https://dummyjson.com/products?limit=20"
try:
    response = requests.get(api_url, timeout=7) # Keeping timeout a bit high
    all_data = response.json()
    product_list = all_data['products']
    
    # Custom Table Header
    print(f"{'ID':<3} | {'Product Name':<30} | {'Price':<8} | {'Rating'}")
    print("-" * 60)
    for p in product_list:
        print(f"{p['id']:<3} | {p['title']:<30} | ${p['price']:<7} | {p['rating']}")

    # Task 2 - Step 2: Filtering and Sorting manually
    print("\n--- Best Products (Rating >= 4.5, Sorted by Price) ---")
    high_rated = []
    for p in product_list:
        if p['rating'] >= 4.5:
            high_rated.append(p)
    
    # Sorting from High price to Low price
    high_rated.sort(key=lambda item: item['price'], reverse=True)
    for p in high_rated:
        print(f"Price: ${p['price']} | Rating: {p['rating']} | {p['title']}")

except requests.exceptions.ConnectionError:
    print("Error: No internet connection.")
    write_to_log("fetch_products", "ConnectionError", "Internet disconnected")
except Exception as err:
    print(f"Something went wrong: {err}")
    write_to_log("fetch_products", "GeneralError", str(err))

# Task 2 - Step 3: Specific category search
print("\n--- Laptop Search ---")
laptop_res = requests.get("https://dummyjson.com/products/category/laptops")
if laptop_res.status_code == 200:
    for lap in laptop_res.json()['products']:
        print(f"Found Laptop: {lap['title']} (Cost: ${lap['price']})")

# Task 2 - Step 4: POST simulation
print("\n--- Testing POST Request ---")
my_item = {"title": "Student Laptop Pro", "price": 1200, "category": "laptops"}
post_call = requests.post("https://dummyjson.com/products/add", json=my_item)
print("Server assigned ID:", post_call.json().get('id'))



# Task 3: Error Handling Practice

print("\n--- TASK 3: SAFE FUNCTIONS ---")

def safe_divide(val1, val2):
    try:
        result = val1 / val2
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print(f"Normal Divide (10/2): {safe_divide(10, 2)}")
print(f"Zero Divide (10/0): {safe_divide(10, 0)}")
print(f"Type Error ('ten'/2): {safe_divide('ten', 2)}")

def read_file_safe(name):
    try:
        # Trying to read the file
        f = open(name, "r")
        content = f.read()
        f.close()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{name}' was not found.")
    finally:
        # finally block is must as per instructions
        print(f"Done: Attempt to read '{name}' finished.")

# Testing the safe reader
read_file_safe("python_notes.txt") # Success
read_file_safe("ghost_file.txt")    # Fail



# Task 3 & 4: Final Loop and Log Display

print("\n--- PRODUCT LOOKUP LOOP ---")

while True:
    entry = input("\nEnter ID (1-100) to find product, or 'quit': ").strip().lower()
    
    if entry == 'quit':
        print("Closing lookup tool...")
        break
    
    # Input validation
    if not entry.isnumeric():
        print("Note: Please enter numbers only!")
        continue
    
    val = int(entry)
    if val < 1 or val > 100:
        print("Note: Product ID must be between 1 and 100.")
        continue
        
    # Calling API for specific product
    check_url = f"https://dummyjson.com/products/{val}"
    lookup_res = requests.get(check_url)
    
    if lookup_res.status_code == 200:
        p_info = lookup_res.json()
        print(f"Result: {p_info['title']} - Price: ${p_info['price']}")
    elif lookup_res.status_code == 404:
        print("Status: Product not found (404).")
        write_to_log("lookup_product", "HTTPError", f"404 for Product ID {val}")

# Triggering a real ConnectionError for Task 4 requirement
print("\nTriggering a connection error for the log...")
try:
    requests.get("https://this-is-a-fake-unreachable-site-123.com", timeout=1)
except:
    write_to_log("test_connection", "ConnectionError", "Fake site unreachable")
    print("Fake error logged.")

# Printing the final error log file
print("\n--- FINAL ERROR LOG CONTENT ---")
final_logs = read_file_safe("error_log.txt")
if final_logs:
    print(final_logs)