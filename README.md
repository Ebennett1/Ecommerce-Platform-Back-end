# JS Arrays & Control Flow Practice
![](https://i.imgur.com/XaudnU3.png)


## Node.js
For this deliverable you'll be using software we installed on the first day of this cohort called Node.js to run JavaScript files in the terminal.


## Setup
1. Fork and clone this repository
2. `cd` into the folder you just cloned
3. Create a file called `solutions.js`
4. To run your `solutions.js` file run the following command in your terminal:
    ```shell
    node solutions.js
    ``` 
    This will use Node.js to read and execute your JavaScript file!
5. Refer back to your class notes, lessons, and videos from today if you need help



## Your Tasks
### 1. Easy Does It
1. Create an array that contains three quotes and store it in a variable called `quotes`.

<hr>
:octocat: Commit message: "Easy does it"
<hr>


### 2. Random
Given the following array `const randomThings = [1, 10, "Hello", true]`
1. how do you access the 1st element in the array?
2. Reassign the value of `"Hello"` to `"World"`.
3. Check the value of the array to make sure it updated the array.

<hr>
:octocat: Commit message: "Interacted with random things"
<hr>


### 3. We've Got Class
Given the following array `const ourClass = ["Stan Lee", "Zoom", "Github", "Slack"]`
1. What would you write to access the 3rd element of the array?
2. Change the value of "Github" to "Octocat"
3. Add a new element, "Cloud City" to the array.

<hr>
:octocat: Commit message: "I've got class"
<hr>


### 4. Mix It Up
1. Given the following array `const myArray = [5 ,10 ,500, 20]`
1. Using the `push` method, add the string `"Egon"` to the end of the array.
1. Using a method, remove the string from the end of the array.
1. Using the `unshift` method, add the string `"Bob Marley"` to the beginning of the array
1. Using a different method, remove the string from the beginning of the array
1. Use the reverse method on this array

<hr>
:octocat: Commit message: "Mixing it up"
<hr>


### 5. Biggie Smalls
Write an `if..else` statement that iterates over the `myArray` array declared above:
1. console.log `little number` if the number is entered is less than **100**
2. If the number entered is 100 or more, alert `big number`.

<hr>
:octocat: Commit message: "Birthdays were the worst days, now we sip champagne when we thirst-ay."
<hr>


### 6. Monkey in the Middle
Write an `if...else if...else` statement:
1. console.log `little number` if the number entered is less than **5**.<br>
2.  If the number entered is more than 10, log `big number`.
3. Otherwise, console.log "monkey".

<hr>
:octocat: Commit message: "Monkey-ing around"
<hr>


### 7. What's in Your Closet?
Below, we've given you examples of Kristyn and Thom's closets modeled as data in JavaScript.
```javascript
const kristynsCloset = [
  "left shoe",
  "cowboy boots",
  "right sock",
  "GA hoodie",
  "green pants",
  "yellow knit hat",
  "marshmallow peeps"
];

// Thom's closet is more complicated. Check out this nested data structure!!
const thomsCloset = [
  [
    // These are Thom's shirts
    "grey button-up",
    "dark grey button-up",
    "light blue button-up",
    "blue button-up",
  ],[
    // These are Thom's pants
    "grey jeans",
    "jeans",
    "PJs"
  ],[
    // Thom's accessories
    "wool mittens",
    "wool scarf",
    "raybans"
  ]
];
```

1. What's Kristyn wearing today? Using bracket notation to access items in `kristynsCloset`, log the sentence "Kristyn is rocking that " + *the third item in Kristyn's closet* + " today!" to the console.
1. Kristyn can't find her left shoe. Remove this item from her closet and save it to a variable named `kristynShoe`.
1. Kristyn just bought some sweet shades! Add `"raybans"` to her closet **after `"yellow knit hat"`.**
1. Kristyn spilled coffee on her hat... modify this item to read `"stained knit hat"` instead of yellow.
1. Put together an outfit for Thom! Using **bracket notation**, access the first element in Thom's `shirts` array.
1. In the same way, access one item from Thom's pants array.
1. Access one item from Thom's accessories array.
1. Log a sentence about what Thom's wearing. Example: `"Thom is looking fierce in a grey button-up, jeans and wool scarf!"`
1. Get more specific about what kind of PJs Thom's wearing this winter. Modify the name of his PJ pants to `Footie Pajamas`.

<hr>
:octocat: Commit message: "Been in the closet for too long"
<hr>


### Bonus
Write a loop that prints the numbers in order
```js
const twoDArray = [
  [9,8,7],
  [6,5,4],
  [3,2,1],
];
```
expect:
```
1
2
3
4
5
6
7
8
9
```
Try using `for of` loops instead of a regular `for` loop - does it make sense for this task?

<hr>
:octocat: Commit message: "Bonus complete!"
<hr>
# Ecommerce-Platform-Back-end
