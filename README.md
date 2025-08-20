# Kamenozrut

## What is Kamenozrut?
Kamenozrut is one of few games in my uni's information system. During boring classes this was my way to make the time pass faster. Goal of this game is to clear the board by clicking on multiple adjacent stones with the same color which disappear after the click. My skill got better after each game, so I naturally wanted to compete and decided I want to code this game and make it multiplayer.

## System design
To create client and server code I used **python**. My client side code is using pygame for easier game development. Client and server are connected through **sockets** in order to reliably receive all the data, because every move matters. Both client and server have **sqlite3 dbs** to save some important data, such as high score, game settings, active users etc. 

## Features of my version
### Custom music and sound effects
I spent a few hours making these two tracks for in-game music, but I think they fit well into the theme. I like some random surprising effect in game, so I added various sound effects on click or in special conditions like winning or losing a game.
### Custom color pallete
For better user experience there is option to choose from four color palletes of stones.
### It doesn't matter if you are offline or online.
Singleplayer with two modes (standard and color madness) are ready for every situation without the internet connection. Your high score is saved and you can stack your score when you win multiple games in a row. 

If you want to compete against other players, you should definitely try multiplayer, where you fight against other people. The ability to get really high score in short amount of time is crucial, but winning is the ultimate decider!
(Multiplayer is still in development, will be updated soon!!)
### Animations 
Buttons are highlighted on hover. Similar mechanic also works with group of stones that are hovered by a player. Can't forget to mention the title screen animation which is very similar to the bouncing DVD logo. 

## Final outcomes
During the development process I learned a lot about sockets, JSON data format, OOP, working with simple database, UI design. I knew about a lot this stuff, but it was a great combination of separate tools that I combined into one project. It was and is still my huge passion to develop games and also improve at coding.
