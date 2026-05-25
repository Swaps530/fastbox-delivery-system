import json
import math


# Function to calculate distance
def calculate_distance(point1, point2):

    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance


# Read JSON file
with open("base_case.json", "r") as file:

    data = json.load(file)


# Store warehouses
warehouses = {}

for warehouse in data["warehouses"]:

    warehouses[warehouse["id"]] = warehouse["location"]


# Store agents
agents = {}

for agent in data["agents"]:

    agents[agent["id"]] = {
        "location": agent["location"],
        "packages_delivered": 0,
        "total_distance": 0
    }


# Get packages
packages = data["packages"]


# Assign packages
for package in packages:

    warehouse_id = package["warehouse_id"]

    warehouse_location = warehouses[warehouse_id]

    destination = package["destination"]

    nearest_agent = None

    minimum_distance = float("inf")


    # Find nearest agent
    for agent_id, agent_info in agents.items():

        agent_location = agent_info["location"]

        distance_to_warehouse = calculate_distance(
            agent_location,
            warehouse_location
        )

        if distance_to_warehouse < minimum_distance:

            minimum_distance = distance_to_warehouse

            nearest_agent = agent_id


    # Warehouse to destination distance
    delivery_distance = calculate_distance(
        warehouse_location,
        destination
    )


    # Total distance
    total_trip_distance = minimum_distance + delivery_distance


    # Update agent data
    agents[nearest_agent]["packages_delivered"] += 1

    agents[nearest_agent]["total_distance"] += total_trip_distance


# Generate report
report = {}

best_agent = None

best_efficiency = float("inf")


for agent_id, agent_info in agents.items():

    packages_delivered = agent_info["packages_delivered"]

    total_distance = round(agent_info["total_distance"], 2)

    if packages_delivered > 0:

        efficiency = round(
            total_distance / packages_delivered,
            2
        )

    else:
        efficiency = 0


    report[agent_id] = {
        "packages_delivered": packages_delivered,
        "total_distance": total_distance,
        "efficiency": efficiency
    }


    # Best agent
    if packages_delivered > 0 and efficiency < best_efficiency:

        best_efficiency = efficiency

        best_agent = agent_id


report["best_agent"] = best_agent


# Save report
with open("report.json", "w") as file:

    json.dump(report, file, indent=4)


# Print report
print(json.dumps(report, indent=4))