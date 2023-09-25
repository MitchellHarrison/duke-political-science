# POLSCI471 Homework 1
# Mitchell Harrison
# 15-Sep-2023

# EXERCISE 1 ####################

# return the sum of two numbers
def exercise_one(x, y):
    return x + y

# EXERCISE 2 ####################

# calculate factorial without recursion to avoid stack overflows for larger n
def exercise_two(n) -> int:
    # check if input can be factorialized
    if isinstance(n, float):
        if ~n.is_integer():
            print("Factorials can only be performed on integers. Returning.")
            return n

    n = int(n) # in case n is a float in the form X.0
    product = 1

    # factorialize
    while n > 1:
        product *= n
        n -= 1

    return product


# EXERCISE 3 ####################

def exercise_three(l:list, n) -> int:
    # check
    for idx in range(len(l)):
        if l[idx] == n:
            return idx

    # if not in list, return -1
    return -1


# EXERCISE 4 ####################

class Person:
    def __init__(self, name:str, original_savings:int, months:int = 120, 
                 rate:float = 0.01):
        self.name = name
        self.original_savings = original_savings
        self.months = months
        self.rate = rate
        self.updated_savings = self.__collect_interest()

    # update savings after 10 years of compounded interest
    def __collect_interest(self) -> float:
        new_savings = self.original_savings

        for _ in range(self.months):
            new_savings *= (1 + self.rate)

        return round(new_savings, 2)

    def display_savings(self) -> None:
        print(
            "{} went from ${} to ${} after {} months at {}% interest.".format(
                self.name, self.original_savings, self.updated_savings, 
                self.months, self.rate
            )
        )


def exercise_four() -> None:
    # create a list of people to simulate interest 
    person1 = Person("Person 1", 100)
    person2 = Person("Person 2", 200)
    person3 = Person("Person 3", 300)
    people = [person1, person2, person3]

    # display solution to exercise 4
    for person in people:
        person.display_savings()


# EXERCISE 5 ####################
# see Bureaucracy_altered.py for Exercise 5
