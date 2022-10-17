import requests
URL="http://ip-api.com/json/"
def locate(IP):
    r = requests.get(URL+IP).json()
    if(r["status"] == "success"):
        print("Successfully Located :",IP)
        print("Country: ", r["country"])
        print("Region: ", r["regionName"])
        print("City: ", r["city"])
        print("ZIP: ", r["zip"])
        print("Latitude: ", r["lat"])
        print("Longitude: ", r["lon"])
        print("Timezone: ", r["timezone"])
        print("ISP: ", r["isp"])
    else:
        print("Error! Please try again.")
IP=input("Enter IP Address To Geolocate: ")
locate(IP)

