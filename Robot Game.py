zones = {
    '1': ['Coins', 'Nothing', 'Power Cell'],
    '2': ['Nothing', 'Power Cell', 'Power Cell'],
    '3': ['Nothing', 'Nothing', 'Key', 'Power Cell'],
    '4': ['Nothing', 'Power Cell', 'Nothing'],
    '5': ['Power Cell', 'Power Cell', 'Power Cell'],
    '6': ['Nothing', 'Nothing', 'Nothing'],
    '7': ['Coins'],
    '8': ['Nothing', 'Nothing', 'Nothing'],
    '9': ['Treasure'],  # Zone 9 that requires a key and all power cells to unlock
    '10': ['Buyable Power Cell']  # Shop Zone where you can buy a Power Cell
}

robot_inventory = []
battery_lvl = 100
has_key = False  # Flag to track if the player has the key
total_power_cells = sum([zone.count('Power Cell') for zone in zones.values()])  # Total number of power cells in the game
power_cell_cost = 3  # Cost of one Power Cell in the shop (Zone 10)

# Function to move to a different zone
def move_to_zone(zone):
    global battery_lvl, has_key
    if zone == '9':
        if 'Key' not in robot_inventory:
            print("You need a key to unlock Zone 9!")
            return
        if robot_inventory.count('Power Cell') < total_power_cells:
            print(f"You need to collect all {total_power_cells} Power Cells before you can unlock Zone 9!")
            return
    
    if zone == '10':
        print("Welcome to the Shop Zone! You can buy a Power Cell here if you have enough Coins.")
        buy_power_cell()
        return

    if zone not in zones:
        print(f"{zone} is not a valid zone.")
        return
    
    print(f"Moving to Zone {zone}...")
    battery_lvl -= 10  # Deduct battery for moving to the zone
    if battery_lvl <= 0:
        print("Battery drained! Game over.")
        return

    print(f"You have entered Zone {zone}.")
    search = input("Would you like to search the zone for hidden items? (yes/no): ").lower()

    if search == 'yes':
        search_zone(zone)
    else:
        print(f"You decided not to search Zone {zone}.")

# Function to search the zone and reveal hidden items
def search_zone(zone):
    items_in_zone = zones[zone]
    if not items_in_zone:
        print("No items found in this zone.")
    else:
        print(f"Items found in Zone {zone}: {', '.join(items_in_zone)}")
    
    item = input("Enter the item you want to collect: ").capitalize()
    collect_item(item, zone)

# Function to collect an item (Coins, Key, Power Cells)
def collect_item(item, zone):
    global battery_lvl, has_key
    if battery_lvl <= 0:
        print("No battery left to collect items. Game over.")
        return
    
    if item in zones[zone]:
        if item == 'Power Cell' or item == 'Coins' or item == 'Key':
            robot_inventory.append(item)
            zones[zone].remove(item)
            print(f"Collected {item} from Zone {zone}.")
            
            if item == 'Key':
                has_key = True
                print("You have collected the key! You can now unlock Zone 9.")
        elif item == 'Nothing':
            print("There's nothing to collect here.")
        else:
            print(f"{item} cannot be collected.")
    else:
        print(f"{item} is not in Zone {zone}.")

    # Deduct battery after collecting an item
    battery_lvl -= 5
    if battery_lvl <= 0:
        print("Battery drained! Game over.")

# Function to buy a Power Cell from the shop (Zone 10)
def buy_power_cell():
    coins_in_inventory = robot_inventory.count('Coins')
    if coins_in_inventory >= power_cell_cost:
        robot_inventory.append('Power Cell')
        # Remove the necessary number of coins from the inventory
        for _ in range(power_cell_cost):
            robot_inventory.remove('Coins')
        print(f"Purchased a Power Cell! It cost you {power_cell_cost} Coins.")
    else:
        print(f"You don't have enough Coins! You need {power_cell_cost} Coins to buy a Power Cell.")
    print(f"Current inventory: {', '.join(robot_inventory)}")

# Function to display the current inventory of Power Cells
def display_power_cells():
    power_cells = robot_inventory.count('Power Cell')
    if power_cells == 0:
        print("No Power Cells collected.")
    else:
        print(f"Collected Power Cells: {power_cells}")

# Function to display the full current inventory
def display_inventory():
    if not robot_inventory:
        print("No items in inventory.")
    else:
        print(f"Current inventory: {', '.join(robot_inventory)}")

# Main game loop
def game():
    global battery_lvl
    print("Welcome to the Robot Power Cell Collection Game!")
    print(f"Battery Level: {battery_lvl}%\n")

    while battery_lvl > 0:
        print("Zones available: 1, 2, 3, 4, 5, 6, 7, 8, 9 (requires key and all power cells), 10 (Shop)")
        zone = input("Enter the zone you want to move to (or type 'inventory' to view collected Power Cells): ")

        if zone.lower() == 'inventory':
            display_power_cells()
            continue

        if zone in zones:
            move_to_zone(zone)

            if battery_lvl > 0:
                if zone == '9' and robot_inventory.count('Power Cell') == total_power_cells:
                    print("Congratulations! You've collected all Power Cells and unlocked Zone 9. You win!")
                    break

                display_inventory()

                # End the game if all power cells are collected and Zone 9 is unlocked
                if all('Power Cell' not in items for items in zones.values()) and zone == '9':
                    print(f"All {total_power_cells} Power Cells collected! You win!")
                    break
        else:
            print(f"Zone {zone} is not valid.")

        print(f"Battery Level: {battery_lvl}%\n")

    if battery_lvl <= 0:
        print("Battery drained! Game over.")

# Start the game
game()
