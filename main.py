from nicegui import ui
import yaml
import netifaces


# Get a list of all the network interfaces
interfaces = netifaces.interfaces()
# Loop over all the interfaces and print their details
# for iface in interfaces:
#     iface_details = netifaces.ifaddresses(iface)
#     print(f"Interface {iface} has details: {iface_details}")

ignore_interfaces = [] #["rtsp2","lo","docker"]
filtered_interfaces = list(filter(lambda iface: all(ignored not in iface for ignored in ignore_interfaces), interfaces))

with open('config.example.yaml') as file :
    config_file = yaml.safe_load(file)


#print(yaml.dump(config_file))

ui.label('Hello NiceGUI! Under development')

#toggle1 = ui.toggle(list(filter(lambda iface: all(ignored not in iface for ignored in ignore_interfaces), interfaces)))

with ui.element("div").classes("columns-5 w-full gap-5"):
    for iface in filtered_interfaces:
        addrs = netifaces.ifaddresses(iface)
        with ui.card().classes("break-inside-avoid"):
            for iface_if in addrs[netifaces.AF_INET]:
                ui.label(iface)
                ui.label(iface_if["addr"])


for device in config_file['onvif']:
    with ui.expansion(device["name"], icon="work").classes("w-full"):
        with ui.row():
            ui.input(label='Camera Name', value=device["name"])
            #ui.input(label='Ethernet Name', value=device["dev"])
            ui.select(label="Interface",  options=interfaces).classes("w-32")

            ui.input(label='Target IP', value=device["target"]["hostname"]) #.tooltip("Test")
            ui.input(label='Target RTSP', value=device["target"]["ports"]["rtsp"])
            ui.input(label='Target Snapshot', value=device["target"]["ports"]["snapshot"])

            ui.input(label='UUID', value=device["uuid"])
            ui.input(label='MAC', value=device["mac"])


editor = ui.codemirror(yaml.dump(config_file), language='Python') #.classes('h-32')

#ui.code().bind_content_from(, "onvif").classes("w-full")




ui.run(dark=True, title='RTSP-2-ONVIF Configuration', port=8880)
    