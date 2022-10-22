# add_yt_links_to_braindump
Add youtube timestamp links to brain dump sections referred to in this video: https://www.youtube.com/watch?v=vBFYI6PaZg4 (Thanks Andrew Kirby)


Now you can more easily navigate the braindump without having to search for a time-stamp in a video on youtube. 
Each section will have it's own, time-stamped link. 

e.g.
```
Gym Launch CEO Alex Hormozi Financial freedom for life
https://www.youtube.com/watch?v=8_qL5oB3BR4&ab_channel=EscapeFitness

1
https://www.youtube.com/watch?v=8_qL5oB3BR4&ab_channel=EscapeFitness&t=0s  <---- Easily clickable link that takes you to the time stamp
00:00:00.000 --> 00:01:00.000
i deal with people who don't have a
million dollars of net worth
who are not
```

#### Requirements
Python 3 or later.

#### Using it
1. Know where your directory of .md files are on your disk. e.g. /home/myusername/downloads/Alex\ Hormozi\ Brain/
2. Download and extract this repository. 
3. CD in the command line to the root of this extracted directory. 
4. Run the following command, replacing the directory name. 
```
python add_yt_links.py -d /home/myusername/downloads/Alex\ Hormozi\ Brain/
```
5. Type 'y' and then enter if you are ok with recursively editing .txt and .md files. 
6. You're done, enjoy. 
