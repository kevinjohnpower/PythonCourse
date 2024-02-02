# Project 2 Basic TTRPG
# Kevin Power 2/2/24
# Program that uses functions to simulate a basic Table Top Role Playing Game
# Will need to generate random numbers. Import the library

import random

# Here is high level pseudo code for overall program:
# Ask user for their character's name
# Loop 4 times
#   Assign value to each of 6 abilities: strength, dexterity, constitution,
#    intelligence, wisdom, charisma. This is done by rolling a six sided die
#    4 times and taking sum of highest three rolls
#   Modify ability value according to D&D5e table
#   Ask User for choice: Attack, Negotiate, Search, Eat
#   if Attack
#     determine if hit (max strength or dexterity + roll of 20 sided die >= 12)
#     calculate damage
#     otherwise miss
#   if Negotiate
#     determine if negotiations successful (charisma + roll of 20 sided die >=15)
#     otherwise negotiations unsuccessful
#   if Search
#     determine if treasure found (max intelligence or wisdom + roll of 20 sided die >=12)
#     assign random treasure
#     otherwise no treasure found
#   if Eat
#     food is rancid
#     determine if food will not harm (constitution + roll of 20 sided die >= 10)
#     otherwise food will result in sickness
# End loop


# Function to return character name from user input
def get_name():
    character_name = input("Please enter your characters name:> ")
    return character_name
    
# Function to return a die roll. Die can be arbitrary number of number_sides
# Roll is simulated using random integer function
# Range of output dependent on number of sides passed as an argument
def roll_dice(number_sides):
    roll = random.randint(1,number_sides)
    return roll

# Function to calculate rolling 6 sided die 4 times and taking sum of highest three rolls
# Pseudo code:
# Initialize four element array with values 0,1,2,3
# for every element in array
#   array[i] = result from 6 sided die throw
# remove lowest value for array to give three element array
# sum elements of array
# return sum
def sum_of_four_six_sided_dice_with_lowest_dropped():
    rolls = [0,1,2,3]

    for roll in rolls:
        rolls[roll] = roll_dice(6)

    rolls.remove(min(rolls))
    score = sum(rolls)
    return score
        
# Function to modify ability value according to DnD5e table
# Pseudo code
# modified ability score = (raw ability score - 10) // 2
# return modified ability score
def get_ability_modifier(score):
    ability_mod = (score - 10) // 2
    return ability_mod

# Function to obtain user choice
# Pseudo code
# Enter a value between 1 and 4 for Attack, Negotiate, Search, Eat
# If entered value < 1 or > 4
#   prompt user to renter correct value
# return value
def menu():
    action = int(input("Enter action: 1 = Attack, 2 = Negotiate, 3 = Search, 4 = Eat> "))
    if action < 1 or action > 4:
        menu = True
        while menu:
            print("You must enter an action between 1 and 4")
            action = int(input("Enter action: 1 = Attack, 2 = Negotiate, 3 = Search, 4 = Eat> "))
            if action < 1 or action > 4:
                menu = True
            else:
                menu = False
    return action

# Function to return a random treasure type
# Pseudo code
# Define array of treasure_types: Gems, Gold, Diamond, Jade, Dubloons
# treasure = random element of treasure_types
# return treasure
def return_treasure():
    treasure_types = ["Gems", "Gold", "Diamond", "Jade", "Dubloons"]
    treasure = treasure_types[random.randint(0,4)]
    return treasure

# Define the 4 actions so code is easier to read
ATTACK = 1
NEGOTIATE = 2
SEARCH = 3
EAT = 4

character_name = get_name()

# Use a for loop to allow for 4 actions before exiting program
for _ in range(4):
    strength = sum_of_four_six_sided_dice_with_lowest_dropped()
    dexterity = sum_of_four_six_sided_dice_with_lowest_dropped()
    constitution = sum_of_four_six_sided_dice_with_lowest_dropped()
    intelligence = sum_of_four_six_sided_dice_with_lowest_dropped()
    wisdom = sum_of_four_six_sided_dice_with_lowest_dropped()
    charisma = sum_of_four_six_sided_dice_with_lowest_dropped()

    modified_strength = get_ability_modifier(strength)
    modified_dexterity = get_ability_modifier(dexterity)
    modified_constitution = get_ability_modifier(constitution)
    modified_intelligence = get_ability_modifier(intelligence)
    modified_wisdom = get_ability_modifier(wisdom)
    modified_charisma = get_ability_modifier(charisma)

#   for debug purposes, uncomment these print statements
#   print (strength, dexterity, constitution, intelligence, wisdom, charisma)
#   print (modified_strength,modified_dexterity,modified_constitution,modified_intelligence,modified_wisdom,modified_charisma)
    
#   Get users choice of action
    action = menu()
    
    if action == ATTACK:
        score = roll_dice(20)
#       Use max function to find to find best modified ability score
#       Then add it to the result from 20 side die roll
        score += max(modified_strength, modified_dexterity)
        
#       If score is >= 12, hit and calculate damage. Else missed
        if score >= 12:
            print("Congrats", character_name, "you hit")
            damage = max(0, (roll_dice(6) + max(modified_strength,modified_dexterity)))
            print("The total damge was", damage)
        else:
            print("Sorry",character_name,"you missed")
        
    if action == NEGOTIATE:
        score = roll_dice(20) + modified_charisma
#       If the dice + modified charisma is >= 15, negotiations successful, else failed
        if score >= 15:
            print("Congrats", character_name, "you sucessfully negotiated a truce")
        else:
            print("Sorry", character_name, "your negotiations were not successful")
    
    if action == SEARCH:
#       Use max function to find to find best modified ability score
#       Then add it to the result from 20 side die roll
        score = roll_dice(20) + max(modified_intelligence,modified_wisdom)
        if score >= 12:
            print("Congrats", character_name, "you found treasure -", return_treasure())
        else:
            print("Sorry", character_name, "you did not find any treasure")

    if action == EAT:
        print("Sorry", character_name, "the food you ate was rancid")
        score = roll_dice(20) + modified_constitution
#       If score is >= 10, constitution strong enough to withstand food
#       Else you get sick
        if score >= 10:
            print("No worry - your constitution was strong enough to handle the food")
        else:
            print("You got sick - stay in bed")










