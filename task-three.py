import csv
import operator
from itertools import chain 
import sys

#This function imports the data files and appends them into a list, which is then returned.
def importData(data_name, file_name, file_number):
    with open(file_name, newline='') as file_number:
        rows = csv.reader(file_number, delimiter=',')
        data_name = []
        for row in rows:
            data_name.append(row)
    return data_name

"""
This function sorts the data imported from the importData() function.
The user can append only the necessary data using the parameters x and y.
"""
def sortData(data, data_type, x, y):
    data_type = []
    i = -1
    for _ in data:
        i += 1
        data_type.append(data[i][x:y])
    data_type.pop(0)
    return data_type

#This function is specifically for creating a list of houses/flats from the data.
def sortHouses(data):
    houses = []
    houses.append(data[0][2:17])
    #from_iterable used for flattening the list.
    houses = list(chain.from_iterable(houses))
    return houses

#This function is called each day to work out which houses/flats will have their food ready for delivery.
def isReadyForDelivery(flat_number, items, week_orders, shopping_list, houses, total_needed, day, shop_completed):
    is_ready = []
    for y in range(len(items)):
        if shop_completed[flat_number] == False:
            if week_orders[y][int(flat_number)] > "0":
                #If an item that is required by the house has not been bought, append 0 to the list.
                if shopping_list[items[y]] < int(week_orders[y][flat_number]):
                    is_ready.append(0)
                #If an item that is required by the house has been bought, append 1 to the list.
                elif shopping_list[items[y]] >= int(week_orders[y][flat_number]):
                    is_ready.append(1)
                #If list contains only 1s, the house's shopping is ready for delivery.
                if 0 not in is_ready and len(is_ready) == total_needed:
                    print("Deliver to " + str(houses[flat_number]) + " on " + day)
                    #Create record of delivery to ensure repeat deliveries are not made.
                    shop_completed[flat_number] = True
                    for y in range(len(items)):      
                        if week_orders[y][int(flat_number)] > "0":
                            #If delivery is being made, remove items from shopping list/cart that have been delivered.
                            shopping_list[items[y]] -= int(week_orders[y][int(flat_number)]) 

"""
This function is used to display the day selected by the user, 
the store(s) they should visit, and the items they should purchase.
"""
def displayDay(store_char, list, day_of_week):
    print("\n" + day_of_week + ":" + "\nGO TO STORE " + store_char + "\nBuy:")
    for key, value in list.items():
        #Printing values in shopping list that need to be purchased on day selected.
        if value > 0:
            print(value, key)
    #Option for user to return to main menu.        
    print("Press enter to return")
    enter = input()
    if enter == "":
        main()

"""
This function is for calculating the amount of individual items needed by each
each household. The return value is then passed into the isReadyForDelivery()
function to calculate whether the inventory held has the items needed
for each household.
"""
def amountNeeded(houses, items, week_orders):
    total_needed = []
    amount_needed = []
    amount = 0
    for x in range(len(houses)):
        for y in range(len(items)):
            #If an item is required, increment the amount needed.
            if week_orders[y][x] > "0":
                amount += 1
                amount_needed.append(amount)
        total_needed.append(len(amount_needed))
        #Reset counters after each household.
        amount = 0
        amount_needed = []

    return total_needed


"""
This function is for checking which items need to be purchased,
and for creating an inventory of the items purchased so the 
data can be display back to the user.
"""
def purchaseShopping(houses, items, availability, stores_dictionary, shopping_list, shopping_day, calc):
    for x in range(len(houses)):
        for y in range(len(items)): 
            quantity = 0        
            if week_orders[y][x] > "0":
                if availability[y][stores_dictionary] == "Y":
                    #Ensure item purchases are not duplicated.
                    difference = (eval(calc))
                    #If inventory doesn't already have a sufficient amount of the item, add item to shopping list.
                    if difference > 0: 
                        quantity = week_orders[y][x]
                        shopping_list[items[y]] += int(quantity)
                        shopping_day[items[y]] += int(quantity)

#This function extracts the week numbers from the CSV file.
def sortWeeks(weeks, data_file, x, y):
    week = data_file[x][y]
    #Remove "quantity" from String.
    week = week.split(' ', 1)[1]
    weeks.append(week)

    return weeks

def main():
    #Import two main data files.
    data_file_one = importData("data_file_one", "DATA CWK SHOPPING DATA WEEK 7 FILE A.csv", "file_one")
    data_file_two = importData("data_file_two", "DATA CWK SHOPPING DATA WEEK 7 FILE B.csv", "file_two")

    #Create list of all items.
    items = sortData(data_file_one, "items", 1, 2)
    items = list(chain(*items))

    weeks = []

    #Getting the week numbers using the weeks() function.
    for x in range(2, 18, 15):
        weeks = sortWeeks(weeks, data_file_two, 1, x)

    first_week = weeks[0]
    second_week = weeks[1]
    week_name_one = first_week + " ORDERS"
    week_name_two = second_week + " ORDERS"

    """
    Create a copy of the items list as a dictionary to create 
    a record of inventory/stock held. Create a copy for each
    day for ease of displaying instructions.
    """
    shopping_list = dict.fromkeys(items,0)
    global monday_shopping_one
    global monday_shopping_two
    global tuesday_shopping_one
    global tuesday_shopping_two
    monday_shopping_one = shopping_list.copy()
    monday_shopping_two = shopping_list.copy()
    tuesday_shopping_one = shopping_list.copy()
    tuesday_shopping_two = shopping_list.copy()

    #Create list showing the item availability of each store.
    availability = sortData(data_file_one, "availability", 3, 7)

    #Create list of all houses/flats
    houses = sortHouses(data_file_two)

    #Create lists for each week's orders.
    week_name_one = sortData(data_file_two, "week_one_orders", 2, 17)
    week_name_two = sortData(data_file_two, "week_two_orders", 17, 33)
    week_name_one.pop(0)
    week_name_two.pop(0)

    """
    Initialising store variables which will be used to calculate
    which store has the most items available which are required 
    by each household.
    """
    store_a = 0
    store_b = 0
    store_c = 0

    global week_orders 

    """
    User menu for selecting week, also allows user to exit program.
    If user selects week one, use week one data and vice versa.
    """
    print("Please select the week:\n1. " + first_week + "\n2. " + second_week + "\n\nPress enter to exit")
    week_selected = input()
    if week_selected == "1":
        week_orders = week_name_one
        week_selected = first_week
    elif week_selected == "2":
        week_orders = week_name_two
        week_selected = second_week
    elif week_selected == "":
        sys.exit()
    else:
        print("Incorrect value entered.")
        main()

    #Display delivery dates for each residence for the week selected.
    print("\n" + week_selected + " DELIVERY DATES FOR EACH HOUSEHOLD:")

    """
    Calculate which store is most useful by working out
    how many items it has available which is needed by
    either of the stores.
    """
    for x in range(len(houses)):
        for y in range(len(items)):      
            if week_orders[y][x] > "0":
                if availability[y][0] == "Y":
                    store_a += 1
                if availability[y][1] == "Y":
                    store_b += 1
                if availability[y][2] == "Y":
                    store_c += 1

    #Create dictionary of stores for ease of printing store name when required.
    stores = {
        "A" : store_a,
        "B" : store_b,
        "C" : store_c,
    }   

    #Store indices needed as a reference for traversing data.
    stores_indices = {
        stores["A"] : 0,
        stores["B"] : 1,
        stores["C"] : 2
    }

    """
    Create list of boolean values to store whether each 
    household's shop has been completed.
    """
    shop_completed = []

    for x in range(len(houses)):
        shop_completed.append(False)
   
    #Sort stores in descending order of items available.
    sorted_stores = sorted(stores.items(), key=lambda kv: kv[1], reverse=True)

    """
    Convert sorted_stores tuple to dictionary so 
    comparison with stores_indices is possible.
    """
    stores_dictionary = {}
    stores_dictionary = dict(sorted_stores)

    for x in stores_dictionary:
        stores_dictionary[x] = stores_indices[stores[x]]

    """"
    Set best_store_char variable to index 0 of sorted_stores 
    which is the best store. Repeat for the other two stores.
    Find the last character of each stores string for displaying store name.
    """
    best_store_char = sorted_stores[0]
    best_store_char = best_store_char[0]
    second_best_store_char = sorted_stores[1]
    second_best_store_char = second_best_store_char[0]
    worst_store_char = sorted_stores[2]
    worst_store_char = worst_store_char[0]

    """
    Display the required shopping for Monday. Visit the cheap store and add items 
    to shopping list (inventory) if required. Also add to Monday's copy of shopping
    (monday_shopping) for ease of displaying data later on.
    """
    purchaseShopping(houses, items, availability, 3, shopping_list, monday_shopping_one, "1")
  
    """
    Call to amountNeeded so that isReadyForDelivery() will have
    total_needed declared and initialised.
    """ 
    total_needed = amountNeeded(houses, items, week_orders)

    #For each house, see if they are ready for delivery after Monday's first shop.
    for x in range(len(houses)):
        isReadyForDelivery(x, items, week_orders, shopping_list, houses, total_needed[x], "Monday", shop_completed)

    remove_shopping = "int(week_orders[y][x]) - int(monday_shopping_one[items[y]])"

    #Complete second shop of Monday, going to the 'best store'.
    purchaseShopping(houses, items, availability, stores_dictionary[best_store_char], shopping_list, monday_shopping_two, 
    remove_shopping)

    #For each house, see if they are ready for delivery after Monday's second shop.
    for x in range(len(houses)):
        isReadyForDelivery(x, items, week_orders, shopping_list, houses, total_needed[x], "Monday", shop_completed)

    remove_shopping += " - int(monday_shopping_two[items[y]])"

    #Complete first shop for Tuesday, visiting the 'second best store' store.
    purchaseShopping(houses, items, availability, stores_dictionary[second_best_store_char], shopping_list, tuesday_shopping_one, 
    remove_shopping)

    #Check if houses are ready for delivery after Tuesday's first shop.
    for x in range(len(houses)):
        isReadyForDelivery(x, items, week_orders, shopping_list, houses, total_needed[x], "Tuesday", shop_completed)
    
    remove_shopping += " - int(tuesday_shopping_one[items[y]])"

    #Complete second shop for Tuesday, visiting the 'worst' store.
    purchaseShopping(houses, items, availability, stores_dictionary[worst_store_char], shopping_list, tuesday_shopping_two,
     remove_shopping)

    #Make final deliveries after Tuesday's shopping.
    for x in range(len(houses)):
        isReadyForDelivery(x, items, week_orders, shopping_list, houses, total_needed[x], "Tuesday", shop_completed)

    #Menu options to display each day's necessary shopping
    print("\nVIEW DAILY SHOPS:\nPlease select the day:\n1. Monday Shop One\n2. Monday Shop Two\n3. Tuesday Shop One\n4. Tuesday Shop Two\n5. Go Back")
    day_selected = input()
    if day_selected == "5":
        main()
    elif day_selected == "1": 
        displayDay("CHEAP STORE", monday_shopping_one, "Monday")
    elif day_selected == "2":
        displayDay(best_store_char, monday_shopping_two, "Monday")
    elif day_selected == "3":
        displayDay(second_best_store_char, tuesday_shopping_one, "Tuesday")
    elif day_selected == "4":
        displayDay(worst_store_char, tuesday_shopping_two, "Tuesday")
    else:
        print("Invalid value entered.")
        main()

if __name__ == "__main__":
    main()