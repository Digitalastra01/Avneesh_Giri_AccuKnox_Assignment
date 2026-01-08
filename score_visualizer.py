import requests
import matplotlib.pyplot as plt
import statistics

# Configuration
API_URL = "https://api.example.com/scores" # Placeholder URL
OUTPUT_FILE = "scores_chart.png"

def fetch_scores_from_api():
    """
    Fetches student scores from the API.
    Uses mock data if usage of the placeholder URL is detected.
    """
    if "api.example.com" in API_URL:
        print("[INFO] Using mock data for demonstration purposes.")
        return [
            {"name": "Avneesh", "score": 85},
            {"name": "Bharath", "score": 92},
            {"name": "Chethan", "score": 78},
            {"name": "Dhruv", "score": 88},
            {"name": "Eshaan", "score": 95},
            {"name": "Gaurav", "score": 67},
            {"name": "Hritik", "score": 72}
        ]

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch data: {e}")
        return []

def process_and_visualize(data):
    if not data:
        print("No data to process.")
        return

    # Extract names and scores
    names = [student['name'] for student in data]
    scores = [student['score'] for student in data]

    # Calculate Average
    avg_score = statistics.mean(scores)
    print(f"Average Score: {avg_score:.2f}")

    # Visualization
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, scores, color='skyblue')
    
    # Add a line for average
    plt.axhline(y=avg_score, color='r', linestyle='--', label=f'Average ({avg_score:.1f})')
    
    plt.xlabel('Students')
    plt.ylabel('Scores')
    plt.title('Student Test Scores')
    plt.legend()
    plt.ylim(0, 100) # Assuming scores are out of 100

    # Add text labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height}',
                 ha='center', va='bottom')

    # Save the chart
    try:
        plt.savefig(OUTPUT_FILE)
        print(f"[SUCCESS] Chart saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"[ERROR] Failed to save chart: {e}")

def main():
    print("Starting Score Visualizer...")
    data = fetch_scores_from_api()
    process_and_visualize(data)

if __name__ == "__main__":
    main()
