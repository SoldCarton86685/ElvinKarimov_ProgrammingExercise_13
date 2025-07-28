import sqlite3
import random
import matplotlib.pyplot as plt

# Initialize database with my initials (G3 for Grok 3)
def create_population_db():
    conn = sqlite3.connect('population_G3.db')
    cursor = conn.cursor()
    
    # Create population table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS population (
            city TEXT,
            year INTEGER,
            population INTEGER
        )
    ''')
    
    # 10 Florida cities with 2023 population data (approximate, based on recent estimates)
    cities_data = [
        ('Miami', 2023, 450000),
        ('Tampa', 2023, 390000),
        ('Orlando', 2023, 310000),
        ('Jacksonville', 2023, 950000),
        ('Tallahassee', 2023, 200000),
        ('Fort Lauderdale', 2023, 185000),
        ('St. Petersburg', 2023, 265000),
        ('Hialeah', 2023, 225000),
        ('Cape Coral', 2023, 200000),
        ('Gainesville', 2023, 140000)
    ]
    
    # Insert initial 2023 data
    cursor.executemany('INSERT INTO population (city, year, population) VALUES (?, ?, ?)', cities_data)
    
    conn.commit()
    conn.close()

# Simulate population growth/decline for 20 years
def simulate_population_growth():
    conn = sqlite3.connect('population_G3.db')
    cursor = conn.cursor()
    
    # Get all cities
    cursor.execute('SELECT DISTINCT city FROM population')
    cities = [row[0] for row in cursor.fetchall()]
    
    for city in cities:
        cursor.execute('SELECT population FROM population WHERE city = ? AND year = 2023', (city,))
        current_pop = cursor.fetchone()[0]
        
        # Simulate for years 2024 to 2043
        for year in range(2024, 2044):
            # Random growth rate between -2% and 5% per year
            growth_rate = random.uniform(-0.02, 0.05)
            current_pop = int(current_pop * (1 + growth_rate))
            cursor.execute('INSERT INTO population (city, year, population) VALUES (?, ?, ?)', 
                         (city, year, current_pop))
    
    conn.commit()
    conn.close()

# Visualize population growth for a selected city
def plot_population_growth():
    conn = sqlite3.connect('population_G3.db')
    cursor = conn.cursor()
    
    # Get list of cities
    cursor.execute('SELECT DISTINCT city FROM population')
    cities = [row[0] for row in cursor.fetchall()]
    
    # Display city options
    print("Available cities:")
    for i, city in enumerate(cities, 1):
        print(f"{i}. {city}")
    
    # Get user input
    while True:
        try:
            choice = int(input("Enter the number of the city to visualize (1-10): "))
            if 1 <= choice <= 10:
                selected_city = cities[choice - 1]
                break
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Fetch population data for the selected city
    cursor.execute('SELECT year, population FROM population WHERE city = ? ORDER BY year', 
                  (selected_city,))
    data = cursor.fetchall()
    
    years = [row[0] for row in data]
    populations = [row[1] for row in data]
    
    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, populations, marker='o')
    plt.title(f'Population Growth for {selected_city} (2023-2043)')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.grid(True)
    plt.show()
    
    conn.close()

# Main execution
if __name__ == "__main__":
    create_population_db()
    simulate_population_growth()
    plot_population_growth()