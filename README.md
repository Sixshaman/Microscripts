# Microscripts
Some quality of life scripts I use in my personal life.

# AppBlockAutoPin

Enters the pin passcode on the AppBlock app pin screen. Saves two files: KeyPart1.txt and KeyPart2.txt. The first file contains 16 different keys, one of which is valid. The second one contains the number of the valid key. This approach is needed for the pin to be remember-proof.

The intended use is:
1. Launch the AppBlock app and go to restricted mode pin enter screen;
2. Launch the script. It will lock the phone and generate the key pair;
3. Rewrite the key pairs on opposite sides of a sheet of paper;
4. Delete the key pair files;
5. Stash the sheet of paper somewhere far away.

Now you have something to restrict you from procrastinating. You can't easily unblock your phone since you'll need that sheet of paper, which is hopefully far enough to care.

If you lose the sheet of paper, you can unblock the phone by using the brute-force unlocker. It takes approximately 10 hours.

Requires ANDROID_SDK_ROOT environmental variable set.

Syntax for blocking on Samsung S20FE: `python appblock_autopin_samsung_s20fe.py`
Syntax for unblocking on Samsung S20FE: `python unlock_bruteforce_samsung_s20_fe.py`

# RollTheDice

Rolls one of the things to do for today, which are taken from the provided file. Useful when you can't decide what to do today. Saves the choice so you can't reroll if you didn't like it, use it on your own risk!

The algorithm has several tweaks:
- It considers the day to start from 6:00 AM instead of 0:00 AM. This is so you could roll past midnight, while it's still probably "today" for you.
- The fairness of the roll is increased by lowering the chance to roll the same thing the 2nd day in a row to 10%. For 3rd day in a row it's lowered further to 1%.
- The fairness of the roll is increased by increasing the chance to roll a thing to 85%, if it hasn't been rolled at all the last week.

Syntax: `python roll_the_dice.py today_example.txt`

# UltraShortTerm

Shuffles the list of short-term objectives to do for today, to protect you from exhausting and make you switch the things you're doing. Each of the things has to be tagged; the things with the same tag never get reordered.

Has several modes:
- Shuffle shuffles the list of objectives, keeping the things with the same tag in the same order;
- Split splits the list of objectives onto sorted groups of the objectives with the same tag;
- Remove removes all objectives with the provided tag from the list;
- Extract puts all objectives with the provided tag on top of the list.

Syntax for shuffling: `python ultra_short_term.py today_example.txt --unite`
Syntax for splitting: `python ultra_short_term.py today_example.txt --split`
Syntax for removing: `python ultra_short_term.py today_example.txt --remove Work`
Syntax for extracting: `python ultra_short_term.py today_example.txt --extract PetProject`
