---
author: Simon Klug
title: Clean Code in Python 
date: 2020-01-23
tags: coding, clean-code, programming, Python, 
---
[TOC]

I currently reading Clean Code by Robert C. Martin. 
This blogpost is a quick summary with some tips how to apply the tips given for Java for Python. 


1. **Refactor *now*.**  
[LeBlanc's Law](https://www.quora.com/What-resources-could-I-read-about-Leblancs-law?share=1) means "Later == Never" 
2. Names are everything (We read more code than we ever write)
   * Variables should be pronounceable 
   * Make them searchable, no more random fixed numbers 
3. Functions should do one thing
   * Maximum of two (!) arguments per function
   * Max 20 Lines per Function
   * one function one abstraction level
   * No Flags as function parameters
   * Readable top down
4. Comments are often failures as they stand for dirty code
5. Error Handling 
   * Start with Testing for Exceptions
   * Plot out function structure with the `try-except`-statement(s)
   * Dont include abitrary Error-Codes with duplicate code snippts trying to catch all errors, just because some 3-rd Party API returns them. Instead wrap the API to combine errors into ones you need to catch.
   * Do not return or pass `null` to/from functions
6. Write tests to learn the API of a 3-rd Party Package
   * The time spent writing these tests is "free" as in you need to spent the time writing tests anyway to learn the API
   * This also goes for Code that does not (yet) exist
7. The three laws of test driven Development are
   * You may not write production code until you have written a failing unit test
   * You may not write of a unit test than is sufficient to fail
   * You may not write more production code than is sufficient to pass the currently failing test
8. Classes should be small enough to be describable in 25 words without using "if, and, or but"
   * Single Responsiblity

## Code Smells
This is simple list of all the code smells described in the book for my self-reference with Python Examples where appropriate.
### Comments
#### C1 - Inappropriate Information  
#### C2 - Obsolote Comment  
#### C3 - Redundant Comment  
#### C4 - Poorly Written Comment  
#### C5 - Commentend-Out Code   
### Environment  
#### E1 -  Build Requires More Than One Step  
#### E2 -  Tests Require More Than One Step  
  
### Functions  
#### F1 - Too Many Arguments  
*Smell:*
```python 
def create_popup(title, content, button, button_text):
   #...
```

*Refactored into a class:*
```python
class Popup:
    def __init__(self, config: dict):
        title = config["title"]
        content = config["content"]
        #...
menu = Popup(
    {
        "title": "Never gonna give you up!",
        "content": "Never gonna let you down",
        #...
      }
```
#### F2 - Output Arguments  
In Python you do not often run into this problem, except when you pass mutable parameters

*Bad:*
```py
def add_three_list_elements(thislist):
    thislist.append(1)
    thislist.append(2)
    thislist.append(3)

emptyList=[]
add_three_list_elements(emptyList)
# emptyList=[1,2,3]
``` 

*Refactored - Return Values:*
```py
def return_three_list_elements():
   return [1,2,3]
emptyList=[]
emptyList.append(return_three_list_elements)
```
#### F3 - Flag Arguments  
*Smell:*
```py
def send_get_request(ssl):
   if ssl: 
      #...
```

*Refactored into two functions:*
```py
def send_unsecure_get_request():
   #...
def send_secure_get_request():
   #...
```
#### F4 - Dead Function  
If a function is never called it is obsolete and should be removed.
  
### General   
#### G1 - Multiple Languages in One Source File  
This is especially true for Web-Development. So no more or less inline CSS or JS-Hacks in HTML Pages?
#### G2 - Obvious Behavior is Unimplemented  
If you ever look at some part of code and you are surprised, yep, that's a smell. Instead, make the things do things one would except by following the [Principle of Least Astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment).
#### G3 - Incorrect Bahvior at the Boundaries  
Circumvent this by testing also for boundary cases.
#### G4 - Overwridden Safeties  
#### G5 - Duplication  
> Every time you see duplication in the code, it represents a missed opportunity for abstraction.

Indicators of repetition are `if/elif/else`-Statemensts
#### G6 - Code at Wrong Level of Abstraction  
#### G7 - Base Classes Depending on Their Derivatives  
#### G8 - Too Much Information  
#### G9 - Dead Code 
Code is never called. Therefore it is obsolete and should be removed.
#### G10 - Vertical Separation  
Define (local) variables just were you need them.
#### G11 - Inconsistency  
#### G12 - Clutter   
#### G13 - Artificial Coupling  
#### G14 - Feature Envy  
#### G15 - Selector Arguments  
[Look at F3](#f3-flag-arguments)
#### G16 - Obscured Intent
* **[Magic Numbers](#g25-replace-magic-numbers-with-named-constants)**  

* **[Hungarian Notation](https://en.wikipedia.org/wiki/Hungarian_notation)**  
  `emptyList=[]`, `strName="Simon"` 

#### G17 - Misplaced Responsibility  
#### G18 - Inappropriate Static  
#### G19 - Use Explanatory Variables  
Make your programm readable by breaking up your code into intermediate values held in variables with meaningful names.
#### G20 - Functions Names Should Say What They Do  
#### G21 - Understand the Alorithm  
#### G22 - Make Logical Dependencies Physical  
#### G23 - Prefer Polymorphism to If/Else or Switch/Case  
#### G24 - Follow Standart Conventions  
#### G25 - Replace Magic Numbers with Named Constants  
*Smell*:  
```py
time.sleep(604800)
```
*Refactored:*   
```python
seconds_in_a_week = 60*60*24*7
time.sleep(seconds_in_a_week)
```
#### G26 - Be Precise  
#### G27 - Structure over Convention  
#### G28 - Encapsulate Conditionals  
#### G29 - Avoid Negative Conditionals  
#### G30 - Function should do one Thing  
#### G21 - Hidden Tempral Couplings  
#### G32 - Don't be Arbitrary  
#### G33 - Encapsulate Bounary Conditions  
#### G34 - Functions should Descend only one Level of Abstraction  
#### G35 - Keep Configurable Data at High Levels  
#### G36 - Avoid Transitive Navigation


### Names
#### N1 - Choose Descriptive Names
#### N2 - Choose Names ath the Appropriate Level of Abstraction
#### N3 - Use Standard Nomenclature Where Possible
#### N4 - Umambigous Names
#### N5 - Use Long Names for Long Scopes
#### N6 - Avoid Encodings
#### N7 - Names Shoudl Describe Side-Effects

### Tests
#### T1 - Insufficient Tests
#### T2 - Use a Coverage Tool!
#### T3 - Don't Skip Trivial Tests
#### T4 - An Irgnored Test is a Question about an Ambiguity
#### T5 - Test Boundary Conditions
#### T6 - Exhaustively Test Near Bugs
#### T7 - Patterns of Failure Are Revealing
#### T8 - Test Coverage Patterns Can be Revealing
#### T9 - Tests should be fast