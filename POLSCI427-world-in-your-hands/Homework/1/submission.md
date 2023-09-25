# Homework 1 
#### Mitchell Harrison


1. Write a function that returns the sum of two numbers.
```python
# EXERCISE 1 ####################
# return the sum of two numbers
def exercise_one(x, y):
    return x + y
```

---

2. Write a function that calculates the factorial of a given integer.
```python
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
```
    
---

3. Write a function that returns the index of the first occurrence of number *n*
in a list. If *n* does not exist return -1. Do this the long way: that is, do not 
use functions defined for lists to do this for you.
```python
# EXERCISE 3 ####################
def exercise_three(l:list, n) -> int:
    # check
    for idx in range(len(l)):
        if l[idx] == n:
            return idx

    # if not in list, return -1
    return -1
```

---

4. Write a program to replicate a bank. Have it create three people and 
initialize them with $100, $200, and $300, respectively. Calculate how much each
has after 10 years if interest is compounded monthly at a rate of 1% per month. 
Print these three numbers to the screen in a clear way: i.e., don’t just print
the numbers, also tell the viewers what they’re seeing
```python
# EXERCISE 4 ####################
class Person:
    def __init__(self, name:str, original_savings:int, months:int = 1200, 
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
```

---

5. Turn to the template model (bureaucracy.py) we examined in class. Copy the
code to a different file and then, using the existing code as a template, add a 
parameter to each person that alters in some fashion the manner in which the 
person interacts with the model. In addition to adding the parameter to the
definition of a person, this entails altering relevant methods and functions that 
describe how people behave, so that they respond to your new parameter in some
fashion. You must use at least one conditional statement in doing so. In your
problem set, describe your addition substantively and provide the new lines of
code (along with the line of code before and after it to provide context).

In my model, I added two new parameters to the baseline provided in
`Bureaucracy.py`. In the code, they are called `ext_std_dev` and `ext_mean`, and
they represent the power of deliberate foreign actors over a population's 
decision making. This could be anything from foreign disinformation campaigns on
domestic social media, foreign propaganda online or in the media, or any other
deliberate foreign acts in that vein. For simplicity's sake, I've given this new
parameters distributions equal to `bstdev` and `bmean`, respectively.

I've had to change too many lines of code to explicity write each one here, but 
for ease of grading, ive commented above each changed line the word "CHANGED" and
a small explanation as to why I made each change. For example:
```py
# CHANGED: declare new variables ext_std_dev and ext_mean
```
One such change involves modifying the conditional statement that decided whether
or not an actor will act to include if `b` is sufficiently large *or* if my new 
variable `d` (calculated in the same way as `b`) is sufficiently large, or both.

The code runs without crashing, and generates data successfully. Note: no new 
columns have been added to the output of the software. 
