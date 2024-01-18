# GLOBAL VARIABLE to store the file name for which the data will be read from. This way it is easier to alter the map
FILE_NAME = "Map.txt"

def read_data(file_name):
    # Open the file
    file = open(file_name, 'r')

    # Read lines and split into a list
    lines = file.read().splitlines()

    # Close the file
    file.close()

    # Return list of lines
    return lines
    
def create_rooms(l : list) -> list:
    # create empty list
    function_list = []
    
    # for loop that loops through lines [4,24) which store the information of the room
    for i in range (4,24):
        # splitting the line into name, description and connections
        temp = [l[i].split(':')[0], l[i].split(':')[1].split('|')[0]]
        # adding each room (with its splits) into the multidimensional list
        function_list.append(temp)
    
    # returning list of lists of rooms information
    return function_list
    
def add_items(l : list, data : list) -> None:
    # for loop that loops through lines [24,34) which store the information about items
    for i in range(24,34):
        # splitting the data so that the list created stores the index of the room the item is in, its name, and its description
        split = data[i].split(':')
        
        #appending to each room that has an item its item and its item's description
        l[int(split[0])].append(split[1])
        l[int(split[0])].append(split[2])

def create_adjacency_list(data : list) -> list:
    #creating an adjency list using a for loop that will initialize 20 empty lists within the list, each will represent the rooms connections
    adjacency_list = [[] for _ in range(20)] 

    # Append connections between rooms
    # Format: [(destination_room_index, direction), repeat for each connection]
    
    # for loop that will iterate through lines [4,24), which store each rooms information, including their connections
    for i in range(4,24):
        #creating a temporary variable that will store a list of room connections that would look something like this -> ['Room Name:Description','N', '1', 'N', '', etc for each connection..]
        temp = data[i].split('|')
        
        # Removing room name and description -> ['N', '1', 'N', '', etc for each connection..]
        temp.pop(0)
        
        # Removing the duplicates within the list (double N's for North, etc.) -> ['N', '1', '', etc for each connection..]
        temp = remove_duplicates_ordered(temp)
        
        # Removing '' from list -> ['N', '1', etc for each connection..]
        temp.remove('')
        
        # testing **ignore***
        # print(temp)
        
        # for loop that will iterate through the length of list holding the connections but skipping by 2
        for j in range(0,len(temp),2):
            # appending to the adjacency_list a tuple. The tuple will store the index of the area connected to the specific area and the connection direction (N, S, etc.)
            adjacency_list[i-4].append((temp[j+1], temp[j]))

    # returning the adjecency list
    return adjacency_list

def remove_duplicates_ordered(input_list : list) -> list:
    # list to store the unique elements
    unique_elements = []
    
    # for loop that will iterate through each element in the list
    for item in input_list:
        # if the current element is not in the unique elements list, append it to the list
        if item not in unique_elements:
            unique_elements.append(item)
            
    # return list of unique elements
    return unique_elements

def move_rooms(current : int, direction : str, valid_directions : list, valid_rooms: list) -> int:
    # make sure the direction is available
    if direction[0] in valid_directions:
        # return the new room index
        return valid_rooms[valid_directions.index(direction[0])]
    else: 
        # tell user to room is in this direction
        print("No area is in this direction.\n")
        # return the same room index
        return current

def run_game(m : list, rooms : list) -> None:
    # Print intro to the game
    print('\033c') #-> clears console
    print("""Welcome to 'Mysteries of the Enchanted Mansion'

You find yourself standing before the imposing gates of the Enchanted Mansion, a mysterious and ancient abode nestled within the heart of a dense, foreboding forest. Legends speak of the mansion's magical history and the secrets it holds within its grandiose walls. A sense of anticipation and curiosity lingers in the air as you step through the ornate entrance.

Your adventure begins now, intrepid explorer! To navigate through the labyrinthine corridors and unveil the secrets concealed within the mansion, you'll need to use the cardinal directions – North, East, South, and West – to traverse rooms. Stairs beckon with the promise of hidden passages – climb Up to ascend and Down to descend, discovering new levels of the mansion.

But beware, for this mansion is not just a physical space; it is a realm of enchantment and wonder. As you explore, don't forget to look closely at the details around you. Some rooms harbor treasures and curiosities waiting to be uncovered. When you encounter a point of interest, type 'examine' to reveal the secrets it holds. Perhaps a dusty old bookshelf conceals a forgotten tome or an antique chest harbors a long-lost relic.

As you unearth these mysteries, your backpack will become a repository for the mystical artifacts you collect. Type 'backpack' at any time to peer into its depths and marvel at the wonders you've gathered on your journey.

The Enchanted Mansion is a world of both peril and promise. Your choices shape the narrative, and each room holds the potential for a new revelation. Will you uncover the truth hidden within these walls, or will the mysteries of the Enchanted Mansion remain shrouded in magic and myth? The adventure awaits, brave soul – step forth and embark on your quest into the unknown!

If you ever want to leave this enchanted place, type 'leave' and you will be teleported outside this enchanted program!

--------------------------------------------------------------------------      
""")

    # initializing backpack
    backpack = {}
    # intializing current room index
    curr_room = 0

    # while loop that runs forever, within the loop there will be a condition to break out the loop
    while True:
        # setting curr room to int as this was causing errors
        curr_room = int(curr_room)
        
        # print information about current room
        print(f'You are currently in The {rooms[curr_room][0]}.\n{rooms[curr_room][1]}\n')
        
        # getting input from user
        user_input = input(">>").upper()
        
        # getting valid directions and rooms from this current room
        list_of_valid_directions = valid_directions(curr_room, m)
        list_of_valid_rooms = valid_rooms(curr_room, m)
        
        # if structure to decipher the user's input to actions
        if user_input in ['NORTH', 'EAST', 'SOUTH', 'WEST', 'UP', 'DOWN']:
            # update room
            curr_room = move_rooms(curr_room, user_input, list_of_valid_directions, list_of_valid_rooms)
        elif user_input == 'LEAVE':
            # leave the program
            break
        elif user_input == 'EXAMINE':
            # if there are no rooms move on
            if len(rooms[curr_room]) < 3:
                print('There are no items in this area.\n')
                continue
            
            # if the item has already been examined
            if rooms[curr_room][2] in backpack:
                print(f"\nYou are currently examining The {rooms[curr_room][2]}. For more details, type 'Backpack'.")
            # item has not yet been examined
            else:
                print(f"\nYou are currently examining The {rooms[curr_room][2]}.\n{rooms[curr_room][3]}\n")
                temp_dict = {rooms[curr_room][2] : rooms[curr_room][3]}
                # updating backpack
                backpack.update(temp_dict)
        # print user's backpack
        elif user_input == 'BACKPACK':
            print(f"Here is your backpack:\n\n{backpack}")
        # dealing with other inputs
        else:
            print("Your entry is invalid. Here are the valid inputs: North, East, South, West, Up, Down, Leave, Examine, and Backpack\n")

def valid_directions(index : int, room_map : list) -> list:
    directions = []
    
    # for each index in the map
    for i in range(len(room_map[index])):   
        #append the directions that are available
        directions.append(room_map[index][i][1])
    return directions
    
def valid_rooms(index : int, room_map : list) -> list:
    rooms = []
    
    # for each index in the map
    for i in range(len(room_map[index])):   
        # append the rooms that are accessible
        rooms.append(room_map[index][i][0])
    
    return rooms    
    
def main() -> None:
    # calling read_data and giving it the file name. Storing the data in a variable named 'data'
    data = read_data(FILE_NAME)
    
    # calling create_rooms function and passing it the data list and storing the rooms in  variable named 'rooms'
    rooms = create_rooms(data)
    
    # calling add_items to add items to the rooms
    add_items(rooms, data)
    
    # creating an adjecency list representation of a map by calling the create_adjacency_list function and passing it the data file. Storing list in 'the_map'
    the_map = create_adjacency_list(data)
    
    # ***testing ignore***
    #print(the_map)    
    
    # running game by calling run_game function
    run_game(the_map, rooms)
    
    

# calling main function to run the program
main()    