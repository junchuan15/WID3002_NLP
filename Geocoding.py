import requests

def get_location_coordinates(location_name, api_key):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location_name,
        "key": api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data['status'] == 'OK':
        results = data['results'][0]
        formatted_address = results['formatted_address']
        location = results['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return formatted_address, latitude, longitude
    else:
        print("Error:", data['status'])
        return None, None, None

def get_nearby_places(latitude, longitude, api_key, radius):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "key": api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data['status'] == 'OK':
        places = data['results']
        return places
    else:
        print("Error:", data['status'])
        return None

def main():
    api_key = "AIzaSyCaWAF9DCj2P6d6asrh-b61BNua3zD2gMQ"
    location_name = "Dewan Tunku Canselor"
    address, latitude, longitude = get_location_coordinates(location_name, api_key)
    if address is not None:
        print(f"Address: {address}")
        radius = 400  
        places = get_nearby_places(latitude, longitude, api_key, radius)
        if places:
            print("Nearby Places")
            for place in places:
                place_name = place['name']
                place_address = place.get('vicinity', 'Address not available')
                if "Universiti Malaya" in place_address:
                    print(f"- {place_name}")

        else:
            print("No nearby places found within the specified area.")
    else:
        print("Failed to retrieve the location information.")

if __name__ == "__main__":
    main()
