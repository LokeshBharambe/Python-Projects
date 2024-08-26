import phonenumbers
from phonenumbers import carrier, geocoder as phonenumbers_geocoder, timezone
import folium
from opencage.geocoder import OpenCageGeocode
import webbrowser
from tkinter import *
from tkinter import messagebox
import threading
import csv

class PhoneLocatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Number Locator")
        self.root.configure(bg='#2E4053')
        self.root.geometry("500x550")
        self.api_key = "5e05c7a6951c4cdda002c8914563b6f6"
        #self.api_key="d2b3af88e38b4b5bb6e04f77a89e39f3"     # got it froa m youtube but its not working
        self.opencage_geocoder = OpenCageGeocode(self.api_key)
        self.map_file = None

        self.result_text = StringVar()
        self.result_text.set("")

        self.create_widgets()

    def create_widgets(self):
        header_frame = Frame(self.root, bg='#34495E')
        header_frame.pack(fill=X)
        Label(header_frame, text="Phone Number Locator", font=("Arial", 20, "bold"), bg='#34495E', fg='white').pack(pady=10)

        input_frame = Frame(self.root, bg='#2E4053')
        input_frame.pack(pady=20)
        Label(input_frame, text="Enter Phone number with country code (+xx xxxxxxxxx):", font=("Arial", 12), bg='#2E4053', fg='white').pack(pady=10)
        self.entry = Entry(input_frame, width=30, font=("Arial", 12))
        self.entry.pack(pady=10)

        self.search_icon = PhotoImage(file="icons8-search-64.png")
        Button(input_frame, image=self.search_icon, command=self.locate_phone_thread, bg='#2E4053', borderwidth=0).pack(pady=10)

        Button(input_frame, text="Open Map", command=self.open_map, font=("Arial", 12), bg='#2980B9', fg='white', borderwidth=0).pack(pady=10)
        Button(input_frame, text="Save Results", command=self.save_results, font=("Arial", 12), bg='#2980B9', fg='white', borderwidth=0).pack(pady=10)

        result_frame = Frame(self.root, bg='#2E4053')
        result_frame.pack(pady=20)
        Label(result_frame, textvariable=self.result_text, font=("Arial", 12), bg='#2E4053', fg='white').pack(pady=10)

        Label(self.root, text="@lokesh", bg='#2E4053', fg='white').pack(side=BOTTOM, pady=10)

    def locate_phone_thread(self):
        threading.Thread(target=self.locate_phone).start()

    def locate_phone(self):
        mobileNo = self.entry.get()
        self.result_text.set("Processing...\n")
        try:
            mobileNo = phonenumbers.parse(mobileNo)
        except phonenumbers.NumberParseException:
            self.result_text.set("Invalid phone number format.\n")
            return

        if phonenumbers.is_valid_number(mobileNo):
            time_zones = timezone.time_zones_for_number(mobileNo)
            result = f'Phone Number belongs to region: {time_zones}\n'

            service_provider = carrier.name_for_number(mobileNo, "en")
            result += f'Service Provider: {service_provider}\n'

            country_code = phonenumbers.region_code_for_number(mobileNo)
            region_description = phonenumbers_geocoder.description_for_number(mobileNo, "en")
            result += f'Region Description: {region_description}\n'

            query = f"{region_description}, {country_code}"
            results = self.opencage_geocoder.geocode(query)

            if results and len(results):
                location = results[0]['geometry']
                lat, lng = location['lat'], location['lng']
                result += f'Latitude: {lat}, Longitude: {lng}\n'

                # Create a map with folium
                phone_map = folium.Map(location=[lat, lng], zoom_start=10)
                folium.Marker([lat, lng], popup=f"{region_description} ({service_provider})").add_to(phone_map)

                # Save the map to an HTML file
                self.map_file = "phone_location_map.html"
                phone_map.save(self.map_file)
                result += "Map has been saved as phone_location_map.html\n"
            else:
                result += "Could not find the location coordinates for the given phone number.\n"
        else:
            result = "Please enter a valid mobile number.\n"

        self.result_text.set(result)

    def open_map(self):
        if self.map_file:
            webbrowser.open(self.map_file)
        else:
            messagebox.showerror("Error", "Map file not found. Please search for a phone number first.")

    def save_results(self):
        results = self.result_text.get()
        if results:
            with open("phone_locator_results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Results"])
                writer.writerow([results])
            messagebox.showinfo("Success", "Results saved to phone_locator_results.csv")
        else:
            messagebox.showerror("Error", "No results to save.")

if __name__ == "__main__":
    root = Tk()
    app = PhoneLocatorApp(root)
    root.mainloop()
