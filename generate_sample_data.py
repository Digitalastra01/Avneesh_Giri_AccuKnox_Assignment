import csv
import random

FILENAME = "users.csv"
NUM_USERS = 20

def generate_csv():
    print(f"Generating {NUM_USERS} sample users in {FILENAME}...")
    
    with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "email"]) # Header
        
        for i in range(1, NUM_USERS + 1):
            name = f"User {i}"
            email = f"user{i}@example.com"
            writer.writerow([name, email])
            
        # Add a duplicate for testing
        writer.writerow(["Duplicate User", "user1@example.com"])
        print("Added 1 duplicate entry for testing.")

    print(f"[SUCCESS] {FILENAME} created.")

if __name__ == "__main__":
    generate_csv()
