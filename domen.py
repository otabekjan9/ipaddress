import tkinter as tk
from tkinter import ttk, filedialog
import requests
import socket
import time
import threading
import pandas as pd
from queue import Queue

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def scan_ip():
    target = ip_entry.get()
    if is_valid_ip(target):
        # If target is an IP address
        t_IP = target
    else:
        # If target is a domain name, resolve it to IP address
        t_IP = socket.gethostbyname(target)
        
    try:
        payload = {'key': 'EDCB16195A4ADD175246575E74F0FC77', 'ip': t_IP, 'format': 'json'}
        api_result = requests.get('https://api.ip2location.io/', params=payload)
        if api_result.status_code == 200:
            data = api_result.json()
            ip = data.get("ip")
            country = data.get("country_code")
            country_name = data.get("country_name")
            region_name = data.get("region_name")
            city_name = data.get("city_name")
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            time_zone = data.get("time_zone")
            asn = data.get("asn")
            as1 = data.get("as")
            isp = data.get("isp")
            domain = data.get("domain")
            net_speed = data.get("net_speed")
            idd_code = data.get("idd_code")
            area_code = data.get("area_code")
            weather_station_code = data.get("weather_station_code")
            weather_station_name = data.get("weather_station_name")
            mcc = data.get("mcc")
            mnc = data.get("mnc")
            mobile_brand = data.get("mobile_brand")
            elevation = data.get("elevation")
            usage_type = data.get("usage_type")
            address_type = data.get("address_type")
            ads_category = data.get("ads_category")
            ads_category_name = data.get("ads_category_name")
            district = data.get("district")

            result_tree.delete(*result_tree.get_children())
            result_tree.insert("", "end", values=("IP:", ip))
            result_tree.insert("", "end", values=("Country:", country))
            result_tree.insert("", "end", values=("Country Name:", country_name))
            result_tree.insert("", "end", values=("Region Name:", region_name))
            result_tree.insert("", "end", values=("City Name:", city_name))
            result_tree.insert("", "end", values=("Latitude:", latitude))
            result_tree.insert("", "end", values=("Longitude:", longitude))
            result_tree.insert("", "end", values=("Time Zone:", time_zone))
            result_tree.insert("", "end", values=("ASN:", asn))
            result_tree.insert("", "end", values=("AS:", as1))
            result_label.config(text="Ma'lumotlar muvaffaqiyatli olindi", fg="green")  

    except Exception as e:
        result_label.config(text="Xatolik: " + str(e), fg="red")


def download_excel():
    target = ip_entry.get()
    if is_valid_ip(target):
        # If target is an IP address
        t_IP = target
    else:
        # If target is a domain name, resolve it to IP address
        t_IP = socket.gethostbyname(target)
        
    try:
        payload = {'key': 'EDCB16195A4ADD175246575E74F0FC77', 'ip': t_IP, 'format': 'json'}
        api_result = requests.get('https://api.ip2location.io/', params=payload)
        if api_result.status_code == 200:
            data = api_result.json()
            ip = data.get("ip")
            country = data.get("country_code")
            country_name = data.get("country_name")
            region_name = data.get("region_name")
            city_name = data.get("city_name")
            latitude = data.get("latitude")
            longitude = data.get("longitude")
            time_zone = data.get("time_zone")
            asn = data.get("asn")
            as1 = data.get("as")
            isp = data.get("isp")
            domain = data.get("domain")
            net_speed = data.get("net_speed")
            idd_code = data.get("idd_code")
            area_code = data.get("area_code")
            weather_station_code = data.get("weather_station_code")
            weather_station_name = data.get("weather_station_name")
            mcc = data.get("mcc")
            mnc = data.get("mnc")
            mobile_brand = data.get("mobile_brand")
            elevation = data.get("elevation")
            usage_type = data.get("usage_type")
            address_type = data.get("address_type")
            ads_category = data.get("ads_category")
            ads_category_name = data.get("ads_category_name")
            district = data.get("district")

            df = pd.DataFrame({
                "Property": ["IP", "Country", "Country Name", "Region Name", "City Name",
                             "Latitude", "Longitude", "Time Zone", "ASN", "AS"],
                "Value": [ip, country, country_name, region_name, city_name,
                          latitude, longitude, time_zone, asn, as1]
            })

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if file_path:
                df.to_excel(file_path, index=False)
                result_label.config(text="Ma'lumotlar muvaffaqiyatli Excel formatida saqlandi", fg="green")
            else:
                result_label.config(text="Fayl nomini tanlangmadingiz", fg="red")

    except Exception as e:
        result_label.config(text="Xatolik: " + str(e), fg="red")

def portscan():
    target = ip_entry.get()
    if is_valid_ip(target):
        # If target is an IP address
        t_IP = target
    else:
        # If target is a domain name, resolve it to IP address
        t_IP = socket.gethostbyname(target)
    
    socket.setdefaulttimeout(0.25)
    print_lock = threading.Lock()

    
    
    def scan_port(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((t_IP, port))
            with print_lock:
                print(port, 'open')
                result_tree1.insert("", "end", values=("Ochiq port:", port))
            con.close()
        except:
            pass

    def threader():
        while True:
            worker = q.get()
            scan_port(worker)
            q.task_done()

    q = Queue()
    startTime = time.time()
    for x in range(100):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()
    a = int(port1_entry.get())
    b = int(port2_entry.get())
    for worker in range(a, b):
        q.put(worker)

    q.join()

    print('Olingan vaqt:', time.time() - startTime)


root = tk.Tk()
root.title("IP va DOMEN Manzil Skaneri")
root.config(bg="light green")

label_font = ('Arial', 12)

top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, padx=10, pady=10)
but_frame = tk.Frame(root)
but_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

ip_label = tk.Label(top_frame, text="Ip and Domen Address:", font=label_font)
ip_label.pack(side=tk.LEFT, padx=(0, 10))

ip_entry = tk.Entry(top_frame, font=label_font)
ip_entry.pack(side=tk.LEFT)

port1_entry = tk.Entry(but_frame, font=label_font)
port1_entry.pack(side=tk.LEFT)

port2_entry = tk.Entry(but_frame, font=label_font)
port2_entry.pack(side=tk.LEFT)

style = ttk.Style()
style.configure('Custom.TButton', background='blue', foreground='red', font=label_font, borderwidth=0, borderradius=50)

scan_button = ttk.Button(top_frame, text="Skaner", command=scan_ip, style='Custom.TButton')
scan_button.pack(side=tk.LEFT, padx=(10, 0))


result_tree = ttk.Treeview(root, columns=('Property', 'Value'), show='headings')
result_tree.heading('Property', text='Property')
result_tree.heading('Value', text='Result')
result_tree.pack()

result_tree1 = ttk.Treeview(root, columns=('Property', 'Value'), show='headings')
result_tree1.heading('Property', text='Property')
result_tree1.heading('Value', text='Result')
result_tree1.pack()

result_label = tk.Label(root, text='', font=label_font)
result_label.pack(pady=10)


scan_button = tk.Button(but_frame, text="Port scaner", command=portscan, font=label_font, bg="yellow")
scan_button.pack(side=tk.LEFT, padx=(10, 0))



download_button = tk.Button(but_frame, text="Excel yuklab olish", command=download_excel, font=label_font, bg="green", fg="white")
download_button.pack(side=tk.LEFT, padx=(10, 0))

root.mainloop()
