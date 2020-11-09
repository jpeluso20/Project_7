import json,time,os

def main():
    
    # TODO: allow them to choose from multiple JSON files?
    thefiles = os.listdir()
    print(thefiles)
    openfile = input("> ").lower().strip()
    with open(openfile) as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)



def play(rooms):
    start_time = time.time()
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    visited = {}
    
    while True:
        
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        
        
        if current_place in visited:
            print("You've been here before!")
        visited[current_place] = True

        # TODO: print any available items in the room...
        items_here = here['items']
        if len(items_here) >= 1:
            print(items_here)
        
        
        # e.g., There is a Mansion Key.

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        if action == "stuff":
            if len(stuff) > 0:
                print (stuff)
            else:
                print("You have nothing, go get something.")
            continue
        
        if action == "help":
            print_instructions()
            continue
        if action == "search":
            for exit in here['exits']:
                if exit.get("hidden", True):
                    exit["hidden"] = False
            continue
        
        
        # TODO: if they type "stuff", print any items they have (check the stuff list!)
        # TODO: if they type "take", grab any items in the room.
        if action == "take":
            items_here = here['items']
            for x in range(len(items_here)):
                stuff.append(items_here[x])
                items_here.remove(items_here[x])
            continue
        
        if action == "drop":
            drop_item = str(input("What will you drop?"))
            if drop_item in stuff:
                items_here.append(drop_item)
                stuff.remove(drop_item)
            else:
                print("You don't have an item to drop")
            continue
            
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        #if action == "search" or "find":
            
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
       
    print("")
    print("")
    print("=== GAME OVER ===")
    print("It took you")
    print(int(time.time() - start_time))
    print("seconds.")



def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'help' to print the instructions again.")
    print("=== Instructions ===")
    print("")
  

    
if __name__ == '__main__':
    main()
