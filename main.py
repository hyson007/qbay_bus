import streamlit as st
import pandas as pd
import requests
import settings
from datetime import datetime
import pytz

st.set_page_config(layout="wide")


st.title('Q Bay Home')
st.markdown("""
This app retrieves bus arrvial time nearby my home in **Qbay** !
""")

# st.image("girl2.gif", width=300)

col1 = st.sidebar
col2, col3, col4 = st.columns((1,1,1))





col1.header('Input Options')

qbay_bus_stop = {
    "BLK_879B(298)": 75021,
    "Opp_Springfield": 75031,
    "Springfield": 75039,
    "Opp_Tropica": 75251,
    "Tropica": 75259,
    "Santorini": 75409,
}



busStopSelected = col1.multiselect('NearBy Bus stop', 
                            list(qbay_bus_stop.keys()),
                            list(qbay_bus_stop.keys()))



# def getETA(eta):
#     now = datetime.now(pytz.timezone('Asia/Singapore'))
#     if bus.get(field) and bus.get(field).get("EstimatedArrival"):
#         temp = bus.get(field).get("EstimatedArrival")
#         eta_dt = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S%z")
#         # print('eta_dt', eta_dt)
#         delta = eta_dt - now
#         # print('delta', delta)
#         # print('now', now)
#         if delta.seconds > 40000 or delta.seconds < 60:
#             return "arriving"
#         return delta.seconds // 60
#     else:
#         return "NA"

def getBUS(bus_stop):
    hold = {}
    now = datetime.now(pytz.timezone('Asia/Singapore'))
    try:
        querystring = {"BusStopCode":bus_stop}
        response = requests.request("GET", settings.url, headers=settings.headers, 
        params=querystring).json()
        bus_services = response.get("Services")
        # print(bus_services)
    except Exception as e:
        pass
    for bus_service in bus_services:
        bus = bus_service.get("ServiceNo")
        hold[bus] = {}
        first_eta, sec_eta, third_eta = bus_service.get("NextBus"),bus_service.get("NextBus2"),bus_service.get("NextBus3")

        # print(first_eta, sec_eta, third_eta, '============')

        if first_eta:

            temp = first_eta.get("EstimatedArrival")
            eta_dt = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S%z")
            delta = eta_dt - now
            if delta.seconds > 40000 or delta.seconds < 60:
                hold[bus]["NextBus1"] = "ARV"
            else:
                hold[bus]["NextBus1"] = str(delta.seconds // 60)

            # Only proceed if there is first bus ETA.
            temp = sec_eta.get("EstimatedArrival")
            if temp:
                eta_dt = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S%z")
                delta = eta_dt - now
                if delta.seconds > 40000 or delta.seconds < 60:
                    hold[bus]["NextBus2"] = "ARV"
                else:
                    hold[bus]["NextBus2"] = str(delta.seconds // 60)
            else:
                hold[bus]["NextBus2"] = "NA"

            temp = third_eta.get("EstimatedArrival")
            if temp:
                eta_dt = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S%z")
                delta = eta_dt - now
                if delta.seconds > 40000 or delta.seconds < 60:
                    hold[bus]["NextBus3"] = "ARV"
                else:
                    hold[bus]["NextBus3"] = str(delta.seconds // 60)
            else:
                hold[bus]["NextBus3"] = "NA"
        else:
            hold[bus]["NextBus"] = "No Bus"

    # hold["busStop"] = bus_stop
    return pd.DataFrame.from_dict(hold)
        

# list_hold= []

i = 0
for bus_stop_name, bus_stop_number in qbay_bus_stop.items():
    if bus_stop_name in busStopSelected:
        # list_hold.append(getBUS(bus_stop_number))

# final_df = pd.concat(list_hold, axis=0)
# final_df.reset_index()
# final_df.set_index(['busStop'])

# print(final_df.index, final_df.columns)
# st.write(final_df)


        if i %3 ==0:
            col2.write(bus_stop_name)
            col2.write(getBUS(bus_stop_number))
        if i %3 ==1:
            col3.write(bus_stop_name)
            col3.write(getBUS(bus_stop_number))
        if i %3 ==2:
            col4.write(bus_stop_name)
            col4.write(getBUS(bus_stop_number))
        i += 1


