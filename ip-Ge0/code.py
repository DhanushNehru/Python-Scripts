import requests
import csv
import sys

URL = "http://ip-api.com/json/"

def locate_ip(ip):
    try:
        response = requests.get(URL + ip, headers={"User -Agent": "GeoLocator/1.0"})
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        if data["status"] == "success":
            return {
                "IP": ip,
                "Country": data["country"],
                "Region": data["regionName"],
                "City": data["city"],
                "ZIP": data["zip"],
                "Latitude": data["lat"],
                "Longitude": data["lon"],
                "Timezone": data["timezone"],
                "ISP": data["isp"],
            }
        else:
            return {"IP": ip, "Error": "Unable to locate IP address."}
    
    except requests.RequestException as e:
        return {"IP": ip, "Error": str(e)}

def save_to_csv(results, filename='ip_geolocation_results.csv'):
    keys = results[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

def main(ip_addresses):
    results = []
    for ip in ip_addresses:
        result = locate_ip(ip)
        results.append(result)
        print(result)

    # Save results to CSV
    save_to_csv(results)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ip_addresses = sys.argv[1:]  # Get IP addresses from command-line arguments
    else:
        ip_input = input("Enter IP Addresses to Geolocate (comma-separated): ")
        ip_addresses = [ip.strip() for ip in ip_input.split(",")]

    main(ip_addresses)
