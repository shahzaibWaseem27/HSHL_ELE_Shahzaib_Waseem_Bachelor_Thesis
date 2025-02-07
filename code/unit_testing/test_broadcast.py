def broadcast_lora(all_nodes, n=1, determined_building=None, determined_floor=None):


    if determined_building == None and determined_floor == None:

        nodes = list(all_nodes.keys())
        print("Working on all buildings")
                                              
    elif determined_building != None and determined_floor == None:
        
        nodes = list(all_nodes[determined_building].keys())
        print(f"Working on all floors of building {determined_building}")
            
    elif determined_building != None and determined_floor != None:
    
        nodes = list(all_nodes[determined_building][determined_floor])
        print(f"Working on all rooms of floor {determined_floor} of building {determined_building}")
        
    else:
        
        nodes = nodes = list(all_nodes.keys()) 

    for i in range(len(nodes)):
        nodes[i] = int(nodes[i])
        
    print(f"List of working nodes: {nodes}: {type(nodes)}")   

    for node in nodes:
        
        for i in range(n):

            #lora.send_to_wait("broadcast".encode(), node) # location reference nodes don't care what the payload is from the patient. They only forward the RSSI
            # and SNR of this payload to caretaker
            print(f"sent lora packet {i + 1} to node {node}")
            #lora_sent_LED_pin.on()
            #sleep(0.2)
            #lora_sent_LED_pin.off()
            

    #lora.send_to_wait("D, done".encode(), CARETAKER_ADDRESS) #D stands for done, from patient to caretaker, indicating that the broadcast is done
    #lora_sent_LED_pin.on()
    #sleep(0.2)
    #lora_sent_LED_pin.off()


# Updated all_nodes dictionary with globally unique identifiers
all_nodes = {
    1000: {  # Building 1000
        2000: [3000, 3001],  # Floor 2000: Room Nodes 3000, 3001
        2001: [3002, 3003],  # Floor 2001: Room Nodes 3002, 3003
        2002: [3004],        # Floor 2002: Room Node 3004
    },
    1001: {  # Building 1001
        2003: [3005, 3006, 3007],  # Floor 2003: Room Nodes 3005, 3006, 3007
        2004: [3008],              # Floor 2004: Room Node 3008
        2005: [3009, 3010],        # Floor 2005: Room Nodes 3009, 3010
    },
    1002: {  # Building 1002
        2006: [3011],              # Floor 2006: Room Node 3011
        2007: [3012, 3013, 3014],  # Floor 2007: Room Nodes 3012, 3013, 3014
        2008: [3015, 3016],        # Floor 2008: Room Nodes 3015, 3016
        2009: [3017],              # Floor 2009: Room Node 3017
    },
    1003: {  # Building 1003
        2010: [3018, 3019, 3020],  # Floor 2010: Room Nodes 3018, 3019, 3020
        2011: [3021],              # Floor 2011: Room Node 3021
        2012: [3022, 3023],        # Floor 2012: Room Nodes 3022, 3023
        2013: [3024],              # Floor 2013: Room Node 3024
    },
}


# Test Case 1: Broadcast to all buildings
print("Test Case 1: Broadcast to all buildings")
broadcast_lora(all_nodes, n=2)
# Expected Output:
# building nodes extracted
# List of working nodes: [1000, 1001, 1002, 1003]: <class 'list'>
# sent lora packet 1 to node 1000
# sent lora packet 2 to node 1000
# ...
# sent lora packet 2 to node 1003

# Test Case 2: Broadcast to a specific building (Building 1000)
print("\nTest Case 2: Broadcast to all floors in Building 1000")
broadcast_lora(all_nodes, n=2, determined_building=1000)
# Expected Output:
# Working on all floors of building 1000
# List of working nodes: [2000, 2001, 2002]: <class 'list'>
# sent lora packet 1 to node 2000
# ...
# sent lora packet 1 to node 2002

# Test Case 3: Broadcast to a specific floor (Floor 2001 in Building 1000)
print("\nTest Case 3: Broadcast to Floor 2001 in Building 1000")
broadcast_lora(all_nodes, n=3, determined_building=1000, determined_floor=2001)
# Expected Output:
# Working on all rooms of floor 2001 of building 1000
# List of working nodes: [3002, 3003]: <class 'list'>
# sent lora packet 1 to node 3002
# ...
# sent lora packet 3 to node 3003

# Test Case 4: Edge Case with no nodes
print("\nTest Case 4: Edge case with no nodes")
empty_all_nodes = {}
broadcast_lora(empty_all_nodes, n=2)
# Expected Output:
# building nodes extracted
# List of working nodes: []: <class 'list'>

# Test Case 5: Large-scale broadcast to all rooms on a specific floor
print("\nTest Case 5: Large-scale broadcast to all rooms on Floor 2007 in Building 1002")
broadcast_lora(all_nodes, n=3, determined_building=1002, determined_floor=2007)
# Expected Output:
# Working on all rooms of floor 2007 of building 1002
# List of working nodes: [3012, 3013, 3014]: <class 'list'>
# sent lora packet 1 to node 3012
# ...
# sent lora packet 5 to node 3014

# Test Case 6: Single-node broadcast
print("\nTest Case 6: Single-node broadcast (Room Node 3024)")
broadcast_lora(all_nodes, n=2, determined_building=1003, determined_floor=2013)
# Expected Output:
# Working on all rooms of floor 2013 of building 1003
# List of working nodes: [3024]: <class 'list'>
# sent lora packet 1 to node 3024

# Test Case 7: Broadcast to rooms on multiple floors in Building 1001
print("\nTest Case 7: Broadcast to all floors in Building 1001")
broadcast_lora(all_nodes, n=2, determined_building=1001)
# Expected Output:
# Working on all floors of building 1001
# List of working nodes: [2003, 2004, 2005]: <class 'list'>
# sent lora packet 1 to node 2003
# ...
# sent lora packet 1 to node 2005

# Test Case 8: Single-packet broadcast to all buildings
print("\nTest Case 8: Single-packet broadcast to all buildings")
broadcast_lora(all_nodes, n=2)
# Expected Output:
# building nodes extracted
# List of working nodes: [1000, 1001, 1002, 1003]: <class 'list'>
# sent lora packet 1 to node 1000
# ...
# sent lora packet 1 to node 1003

# Test Case 9: Empty floor in a building
print("\nTest Case 9: Empty floor in a building")
all_nodes_with_empty_floor = {
    1004: {  # Building 1004
        2014: [],  # Floor 2014: No rooms
        2015: [3025, 3026],  # Floor 2015: Room Nodes 3025, 3026
    }
}
broadcast_lora(all_nodes_with_empty_floor, n=2)
# Expected Output:
# building nodes extracted
# List of working nodes: [1004]: <class 'list'>
# Working on all floors of building 1004
# List of working nodes: []
# Working on all rooms of floor 2015 of building 1004
# List of working nodes: [3025, 3026]: <class 'list'>
# sent lora packet 1 to node 3025
# ...
# sent lora packet 2 to node 3026

# Test Case 10: Large network with multiple broadcasts
print("\nTest Case 10: Large network broadcast to all rooms")
broadcast_lora(all_nodes, n=4)
# Expected Output:
# building nodes extracted
# List of working nodes: [1000, 1001, 1002, 1003]: <class 'list'>
# sent lora packet 1 to node 1000
# ...
# sent lora packet 10 to node 1003
