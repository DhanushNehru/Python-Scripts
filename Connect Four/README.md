# Connect Four
I have created the board game, "Connect Four", using the programming language Python. The entire project was created all on one file. This was a project I chose to develop during my spare time as this was not a common project constructed by other developers. The program follows all rules of the game, where players can win by either having 4 in a row horizontally, vertically, or diagonally. The dimensions for this particular game is a 6x7 board. In other words, the board is designed as 6 rows and 7 columns. Therefore, I initialized a nested list called board that contains the 7 columns as elements, and the 6 rows within each element. 

```
board = [["-"] * 6, ["-"] * 6, ["-"] * 6, ["-"] * 6, ["-"] * 6, ["-"] * 6, ["-"] * 6]
```


Determining the logic for a player to have 4 in a row diagonally proved to be the most challenging in my opinion. The best solution was to view this as positive and negative slopes since these diagonals were
either from the bottom left to top right, or the top left to bottom right. Afterwards, I created two separate boards to determine all possible coordinates that can be starting points to create 4 in a row as shown
in the table below:

Note: The coordinate is [col, row]

### Positive Slope Possible Starting Points
|            |            |            |            |            |            |            |
|------------|------------|------------|------------|------------|------------|------------|
| <s>1.1</s> | <s>2.1</s> | <s>3.1</s> | <s>4.1</s> | <s>5.1</s> | <s>6.1</s> | <s>7.1</s> |
| <s>1.2</s> | <s>2.2</s> | <s>3.2</s> | <s>4.2</s> | <s>5.2</s> | <s>6.2</s> | <s>7.2</s> |
| <s>1.3</s> | <s>2.3</s> | <s>3.3</s> | <s>4.3</s> | <s>5.3</s> | <s>6.3</s> | <s>7.3</s> |
|    1.4     |    2.4     |    3.4     |    4.4     | <s>5.4</s> | <s>6.4</s> | <s>7.4</s> |
|    1.5     |    2.5     |    3.5     |    4.5     | <s>5.5</s> | <s>6.5</s> | <s>7.5</s> |
|    1.6     |    2.6     |    3.6     |    4.6     | <s>5.6</s> | <s>6.6</s> | <s>7.6</s> |


### Negative Slope Possible Starting Points
|            |            |            |            |            |            |            |
|------------|------------|------------|------------|------------|------------|------------|
|    1.1     |    2.1     |    3.1     |    4.1     | <s>5.1</s> | <s>6.1</s> | <s>7.1</s> |
|    1.2     |    2.2     |    3.2     |    4.2     | <s>5.2</s> | <s>6.2</s> | <s>7.2</s> |
|    1.3     |    2.3     |    3.3     |    4.3     | <s>5.3</s> | <s>6.3</s> | <s>7.3</s> |
| <s>1.4</s> | <s>2.4</s> | <s>3.4</s> | <s>4.4</s> | <s>5.4</s> | <s>6.4</s> | <s>7.4</s> |
| <s>1.5</s> | <s>2.5</s> | <s>3.5</s> | <s>4.5</s> | <s>5.5</s> | <s>6.5</s> | <s>7.5</s> |
| <s>1.6</s> | <s>2.6</s> | <s>3.6</s> | <s>4.6</s> | <s>5.6</s> | <s>6.6</s> | <s>7.6</s> |

What I noticed is the positive slope starting points are from rows 4-6 and columns 1-4, while the negatiive slope starting points are from rows 1-3 and columns 1-4. Therefore, each type of slope has its own
function and nested for loop that iterates through only the possible starting points.