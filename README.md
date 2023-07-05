# Color_Blind_Game

A python bot that will play Instagrams Color Blind Game for you.

# How Color Blind Game Works

In the Color Blind Game you are given a number of different colored circles and you have to click the one that is different.

![Easy Example photo of how to play](https://github.com/themichaelfischer/Color_Blind_Game/tree/main/Photos/_first.png)

As the game progresses it gets increasing hard to decide which circle to pick

![Which circle is correct?](https://github.com/themichaelfischer/Color_Blind_Game/tree/main/Photos/_which_is_correct.png)

![Answer (mouse is on it) ](https://github.com/themichaelfischer/Color_Blind_Game/tree/main/Photos/_this_one.png)

# How a bot helps

The bot is able to look at the rgb values of each circle and compare them enabling it to be able to pick the correct circle

![RGB Values for each circle](https://github.com/themichaelfischer/Color_Blind_Game/tree/main/Photos/match_freeze.png)

With this knowledge the bot is able to pick the circle with the largest rgb variance and click the correct one most of the time.

With this strategy you can get to a score of around 50. However we are aiming for 100.

To combat this we must group the circles that have a low variance from each other minimizing the options to pick from

![Grouped rgb values](https://github.com/themichaelfischer/Color_Blind_Game/tree/main/Photos/_more_obvious_rgb.png)

With this the bot is able to pick the circle with the largest single rgb value variance and variation from the 
average rgb values of all the circles

So while we may still see an image like ![this](https://github.com/themichaelfischer/Color_Blind_Game/tree/main/Photos/_which_2.png)

The computer is able to easily distinguish the correct circle which would look something like ![this](https://github.com/themichaelfischer/Color_Blind_Game/tree/main/Photos/_more_obvious_to_computers_comparing_rgb.png) to use

Here is also a video of how the bot works: https://www.youtube.com/watch?v=PgCkz_Hm1q0
