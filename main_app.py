
from weather import get_weather, save_search_history, display_weather

def main():
    unit = input("Choose temperature unit (C for Celsius, F for Fahrenheit): ").strip().upper()
    unit = 'imperial' if unit == 'F' else 'metric'  # Set unit based on user input

    while True:
        city = input("Enter city name (or 'exit' to quit): ")
        if city.lower() == 'exit':
            break
        
        weather = get_weather(city, unit)
        
        if weather:
            save_search_history(city)
            display_weather(weather, unit)
        else:
            print("City not found or API error. Please try again.")

if __name__ == "_main_":
    main()