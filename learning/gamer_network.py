
# -----------------------------------------------------------------------------
# create_data_structure(string_input):
#   Parses a block of text (such as the one above) and stores relevant
#   information into a data structure. You are free to choose and design any
#   data structure you would like to use to manage the information.
#
# Arguments:
#   string_input: block of text containing the network information
#
#   You may assume that for all the test cases we will use, you will be given the
#   connections and games liked for all users listed on the right-hand side of an
#   'is connected to' statement. For example, we will not use the string
#   "A is connected to B.A likes to play X, Y, Z.C is connected to A.C likes to play X."
#   as a test case for create_data_structure because the string does not
#   list B's connections or liked games.
#
#   The procedure should be able to handle an empty string (the string '') as input, in
#   which case it should return a network with no users.
#
# Return:
#   The newly created network data structure
def create_data_structure(string_input):
    network = {}
    while string_input:
        start_connect = string_input.find('to')
        if start_connect != -1:
            end_connect = string_input.find('.',start_connect)
            friends = string_input[start_connect+2:end_connect+1] # o
            friend_list = []
            while friends.find(' ') != -1:
                start = friends.find(' ')
                comma = friends.find(',',start+1)
                if comma != -1:
                    friend_list.append(friends[start+1:comma])
                    friends = friends[comma+1:]
                else:
                    if friends.find('.',start+1) != -1:
                        end = friends.find('.', start + 1)
                        friend_list.append(friends[start + 1:end])
                        friends = friends[end + 1:]
            #print friend_list
            user_find = string_input.find('likes',end_connect)
            user = string_input[end_connect+1:user_find-1]
            network[user] = [friend_list]
            #print network

            start_hobby = string_input.find('play')
            end_hobby = string_input.find('.', start_hobby)
            hobbys = string_input[start_hobby + 4:end_hobby + 1]
            hobby_list = []
            while hobbys.find(' ') != -1:
                start = hobbys.find(' ')
                comma = hobbys.find(',', start + 1)
                if comma != -1:
                    hobby_list.append(hobbys[start + 1:comma])
                    hobbys =hobbys[comma + 1:]
                else:
                    if hobbys.find('.', start + 1) != -1:
                        end = hobbys.find('.', start + 1)
                        hobby_list.append(hobbys[start + 1:end])
                        hobbys = hobbys[end + 1:]

            network[user].append(hobby_list)
            #print network

            string_input = string_input[end_hobby+1:]
    return network









string_input="John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
Olive likes to play The Legend of Corgi, Starfleet Commander.\
Debra is connected to Walter, Levi, Jennie, Robin.\
Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
Walter is connected to John, Levi, Bryant.\
Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
Levi is connected to Ollie, John, Walter.\
Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
Ollie is connected to Mercedes, Freda, Bryant.\
Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
Jennie is connected to Levi, John, Freda, Robin.\
Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
Robin is connected to Ollie.\
Robin likes to play Call of Arms, Dwarves and Swords.\
Freda is connected to Olive, John, Debra.\
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."

network = create_data_structure(string_input)


# -----------------------------------------------------------------------------
# get_connections(network, user):
#   Returns a list of all the connections that user has
#
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user
#
# Return:
#   A list of all connections the user has.
#   - If the user has no connections, return an empty list.
#   - If the user is not in network, return None.

def get_connections(network, user):
    for users in network:
        if user == users:
            return network[user][0]
    return None

# -----------------------------------------------------------------------------
# get_games_liked(network, user):
#   Returns a list of all the games a user likes
#
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user
#
# Return:
#   A list of all games the user likes.
#   - If the user likes no games, return an empty list.
#   - If the user is not in network, return None.
def get_games_liked(network,user):
    for users in network:
        if users == user:
            return network[user][1]
    return None

#print get_games_liked(network,'John')


# -----------------------------------------------------------------------------
# add_connection(network, user_A, user_B):
#   Adds a connection from user_A to user_B. Make sure to check that both users
#   exist in network.
#
# Arguments:
#   network: the gamer network data structure
#   user_A:  a string with the name of the user the connection is from
#   user_B:  a string with the name of the user the connection is to
#
# Return:
#   The updated network with the new connection added.
#   - If a connection already exists from user_A to user_B, return network unchanged.
#   - If user_A or user_B is not in network, return False.
def add_connection(network, user_A, user_B):
    if user_A in network and user_B in network:
        for friends in network[user_A][0]:
            if friends == user_B:
                return network
            network[user_A][0].append(user_B)
	    return network
    return False

#add_connection(network,'John','Ollie')
#print get_connections(network,'John')


# -----------------------------------------------------------------------------
# add_new_user(network, user, games):
#   Creates a new user profile and adds that user to the network, along with
#   any game preferences specified in games. Assume that the user has no
#   connections to begin with.
#
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user to be added to the network
#   games:   a list of strings containing the user's favorite games, e.g.:
#		     ['Ninja Hamsters', 'Super Mushroom Man', 'Dinosaur Diner']
#
# Return:
#   The updated network with the new user and game preferences added. The new user
#   should have no connections.
#   - If the user already exists in network, return network *UNCHANGED* (do not change
#     the user's game preferences)
def add_new_user(network, user, games):
    if user not in network:
        network[user]=[[],games]
    return network

#print add_new_user(network, "Debra", [])
#print add_new_user(network, "Nick", ["Seven Schemers", "The Movie: The Game"]) # True
#print get_games_liked(network, "Nick")

# -----------------------------------------------------------------------------
# get_secondary_connections(network, user):
#   Finds all the secondary connections (i.e. connections of connections) of a
#   given user.
#
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user
#
# Return:
#   A list containing the secondary connections (connections of connections).
#   - If the user is not in the network, return None.
#   - If a user has no primary connections to begin with, return an empty list.
#
# NOTE:
#   It is OK if a user's list of secondary connections includes the user
#   himself/herself. It is also OK if the list contains a user's primary
#   connection that is a secondary connection as well.
def get_secondary_connections(network, user):
    if user in network:
        first_connection = network[user][0]
        if first_connection:
            secondary_connetcion = []
            for people in first_connection:
                each_secondary = network[people][0]
                for everyone in each_secondary:
                    if everyone not in secondary_connetcion:
                        secondary_connetcion.append(everyone)
            return secondary_connetcion
        return []
	return None

#print get_secondary_connections(network, "Mercedes")

# -----------------------------------------------------------------------------
# count_common_connections(network, user_A, user_B):
#   Finds the number of people that user_A and user_B have in common.
#
# Arguments:
#   network: the gamer network data structure
#   user_A:  a string containing the name of user_A
#   user_B:  a string containing the name of user_B
#
# Return:
#   The number of connections in common (as an integer).
#   - If user_A or user_B is not in network, return False.
def count_common_connections(network, user_A, user_B):
    if user_A in network and user_B in network:
        a_friends = network[user_A][0]
        common = 0
        for each in a_friends:
            if each in network[user_B][0]:
                common = common + 1
        return common
    return False

#print get_connections(network,'Mercedes')
#print get_connections(network,'John')
#print count_common_connections(network, "Mercedes", "John")

#print get_connections(network,'John')



# -----------------------------------------------------------------------------
# find_path_to_friend(network, user_A, user_B):
#   Finds a connections path from user_A to user_B. It has to be an existing
#   path but it DOES NOT have to be the shortest path.
#
# Arguments:
#   network: The network you created with create_data_structure.
#   user_A:  String holding the starting username ("Abe")
#   user_B:  String holding the ending username ("Zed")
#
# Return:
#   A list showing the path from user_A to user_B.
#   - If such a path does not exist, return None.
#   - If user_A or user_B is not in network, return None.
#
# Sample output:
#   >>> print find_path_to_friend(network, "Abe", "Zed")
#   >>> ['Abe', 'Gel', 'Sam', 'Zed']
#   This implies that Abe is connected with Gel, who is connected with Sam,
#   who is connected with Zed.
#
# NOTE:
#   You must solve this problem using recursion!
#
# Hints:
# - Be careful how you handle connection loops, for example, A is connected to B.
#   B is connected to C. C is connected to B. Make sure your code terminates in
#   that case.
# - If you are comfortable with default parameters, you might consider using one
#   in this procedure to keep track of nodes already visited in your search. You
#   may safely add default parameters since all calls used in the grading script
#   will only include the arguments network, user_A, and user_B.
def find_path_to_friend(network, user_A, user_B,step):
	# your RECURSIVE solution here!
    if user_B and user_A in network:
        path = []
        if user_B in network[user_A][0]:
           return user_B
        else:
            if step :
                nextnodes = network[user_A][0]
                for each in nextnodes:
                    path.append(find_path_to_friend(network,each,user_B,step -1)
                    return path

            else:
                return None

    return None


print find_path_to_friend(network, "John", "Olive",1)
#print get_connections(network,'Freda')
#print get_connections(network,'Ollie')
