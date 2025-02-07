p = 0.5
    
def run_tests():
    p = 0.5  # Constant weight for RSSI in score calculation

    # Test Case 1: General case with multiple locations
    # Expected outcome: Location 10
    all_nodes_1 = [
        {"location": 5, "RSSI": -50, "SNR": 10},
        {"location": 5, "RSSI": -45, "SNR": 12},
        {"location": 7, "RSSI": -40, "SNR": 8},
        {"location": 7, "RSSI": -55, "SNR": 9},
        {"location": 10, "RSSI": -30, "SNR": 12},
    ]
    print("Test Case 1:", get_location(all_nodes_1, p))  # Expected: 10

    # Test Case 2: Single node
    # Expected outcome: Location 6
    all_nodes_2 = [
        {"location": 6, "RSSI": -50, "SNR": 10},
    ]
    print("Test Case 2:", get_location(all_nodes_2, p))  # Expected: 6

    # Test Case 3: All nodes have the same location
    # Expected outcome: Location 7
    all_nodes_3 = [
        {"location": 7, "RSSI": -50, "SNR": 8},
        {"location": 7, "RSSI": -45, "SNR": 12},
        {"location": 7, "RSSI": -48, "SNR": 10},
    ]
    print("Test Case 3:", get_location(all_nodes_3, p))  # Expected: 7

    # Test Case 4: Two locations, last node is a different location
    # Expected outcome: Location 8
    all_nodes_4 = [
        {"location": 4, "RSSI": -50, "SNR": 9},
        {"location": 4, "RSSI": -45, "SNR": 12},
        {"location": 8, "RSSI": -40, "SNR": 7},
    ]
    print("Test Case 4:", get_location(all_nodes_4, p))  # Expected: 8

    # Test Case 5: Two locations, last node same as previous
    # Expected outcome: Location 12
    all_nodes_5 = [
        {"location": 12, "RSSI": -50, "SNR": 8},
        {"location": 7, "RSSI": -60, "SNR": 9},
        {"location": 7, "RSSI": -55, "SNR": 10},
    ]
    print("Test Case 5:", get_location(all_nodes_5, p))  # Expected: 12

    # Test Case 6: High RSSI but low SNR
    # Expected outcome: Location 5
    all_nodes_6 = [
        {"location": 5, "RSSI": -20, "SNR": 5},
        {"location": 6, "RSSI": -40, "SNR": 12},
    ]
    print("Test Case 6:", get_location(all_nodes_6, p))  # Expected: 5

    # Test Case 7: Low RSSI but high SNR
    # Expected outcome: Location 10
    all_nodes_7 = [
        {"location": 10, "RSSI": -40, "SNR": 12},
        {"location": 15, "RSSI": -80, "SNR": 5},
    ]
    print("Test Case 7:", get_location(all_nodes_7, p))  # Expected: 10

    # Test Case 8: Equal scores across locations
    # Expected outcome: Location 20
    all_nodes_8 = [
        {"location": 15, "RSSI": -50, "SNR": 8},
        {"location": 20, "RSSI": -50, "SNR": 8},
    ]
    print("Test Case 8:", get_location(all_nodes_8, p))  # Expected: 20 (or 15, depending on implementation)

    # Test Case 9: Floating-point precision
    # Expected outcome: Location 5
    all_nodes_9 = [
        {"location": 5, "RSSI": -50.5, "SNR": 9.2},
        {"location": 5, "RSSI": -45.3, "SNR": 10.1},
        {"location": 10, "RSSI": -60.8, "SNR": 8.7},
    ]
    print("Test Case 9:", get_location(all_nodes_9, p))  # Expected: 5

    

run_tests()