# Kirinus Rewrite

Destiny child stuff related bot based using discord.py rewrite API wrapper.

Here is a overview of Kirinus Functions.

## New Features!
     07/21- [BETA]Waifu game introduced, list units too.

## Commands

Learn more about Kirinus commands:

* [Raid](#raid-command)
* [World Boss](#world-boss-command) (beta)
* [Quotes](#quote-command)
    - [add/edit quote](#adding-quotes:)
    - [remove quote](#removing-a-quote:)
* [Reset](#reset-countdown)
* [Maint](#maint)
* [8 Ball](#8-ball)
* [Slap](#slap:)
* [coin](#coin:)
* [Choose](#choose)
* [Child Search](#child-search)
* [list](#list)
* [Waifu Game](#waifu-game-[beta])

### Gatcha or Gacha

Gives you a random 5* child name that can be obtained or world boss if the argument `wb`  is present.

Usage: `?gatcha` or `?gatcha wb`

Aliases: `Using ?gacha` works too.

### Reset Countdown
Gives the countdown till the next reset.
Use:
`?reset`

![simple reset example](https://cdn.discordapp.com/attachments/242845451739463681/440325135749349377/unknown.png)

### Maint

Works like reset command but will tell you when maint will start/started.

Use: `?maint`

updating maint time (for mods):
`?maint add "MM/DD hh:mm"`

Note that kirinus only accepts kst time.

### Raid Command
To use raid command is very simple:

```?raid [optional:name] [optional: lv] [optional: mention]```

#### The default and simple raid command:

Using only ?raid will print the default raid message with you as default owner:

![simple raid img](https://rodizipa.gitbooks.io/kirinus-docs/content/assets/Default_raid.png)

Of course, if you want to add more info you can use the optional arguments.

#### Adding the name field:

Using the name field will tell us what raid you found. The usage is very simple, you just need to add the name of the raid. If that name have a pic associated on kirinus, the default pic will be replaced.

Using:

```?raid bari```

will return:

![name field img](https://rodizipa.gitbooks.io/kirinus-docs/content/assets/Screenshot_1.png)

Currently the only names that don't have a pic associated are *zelos* and *rudolph*.


#### Adding mention [raid owner] field:

Suppose that u found another person raid, how do you set the owner? Simple, just mention him on the command and Kirinus will do all the hard work.

`?raid nicole @MathBot#7353`

will tell me that the user Math found the raid:

![raid owner img](https://rodizipa.gitbooks.io/kirinus-docs/content/assets/Screenshot_2.png)

**Obs:** The reason i don't keep the mention on the box is because currently on mobile discord, mentions don't appear on embed boxes, instead the user id is displayed. That means that instead of the mention, mobile users will only see numbers. So, using the display name works for now.

#### Adding level field:

Kirinus will try to find numbers on the command line and return it as the raid level.

`?raid santa @MathBot#7353 12` OR `?raid santa 12 @MathBot#7353`

gives back:

![lvl field img](https://rodizipa.gitbooks.io/kirinus-docs/content/assets/Screenshot_3.png)


### World Boss Command

This command makes the reset call automatic, so you don't have to bother.

`?wb start/stop`

`?wb start <id>` ex: `?wb start aria`

Kirinus will give a initial alert and will keep sending ticket alerts each 2 hours.

### Quote Command

Give kirinus a tag and she'll reply with the assigned answer. For this you only need to use:

`?quote <tag>`

Using `?quote docs` will give you a link for this page. Easy right?

#### Listing available quotes:

If you use only quote, or type help/list on second term, kirinus will dm you with the available tags.

`?quote` or `?quote help` or `?quote list`

#### Adding quotes:

Kirinus has ability of adding quotes. For this you only need to obey a certain format.

`?quote add <tag> <content>`

note that on content with spaces, you need to use quotes, otherwise kirinus will only register the first word.

`?quote add test "Some Stuff"`

`Kirinus: Some Stuff`

if you used:

`?quote add test Some Stuff`

`Kirinus:Some`

**obs**: To edit a existent quote, just use `?quote add <tag> <new text>`

#### Removing a quote:

`?quote remove <tag>`

#### Quote Information:
`?quote info <tag>` Will display basic info about the quote creation.

### Slap:
Kirinus will deliver your slap to someone else.

use: `?slap <mention user>`

### Coin:
Flip a coin.

use: `?coin`

### 8 ball
Ask Kirinus about your fortune.

use: `?8ball <question>`

### choose
Make Kirinus choose something for you.

use: `?choose <first choice>, <second choice>, <go on if u want>`

### Child Search
Search for a child skillset by using it's name as argument.

use: `?child name`. Ex: `?child mammon`

Obs: Some childs accept alliases, spaced names must include the whitespace like `?child sang ah`. 
If you can't find the child check [Kirinus Database KR.](https://docs.google.com/spreadsheets/d/1SaZ_QXHhqbRWHYSjY9_g5-TKom-ArxNrjhO_J8DJL7I/edit#gid=0)

### List

In case you want to list all childs in the db and their search terms, or search for a specific term, list can be useful.

Use: 
* `?list` displays all childs in db.
* `?list mona` will search for childs that has mona somewhere on their name.

### Waifu Game [Beta]

Minigame where you finally can declare to the entire server that you're the only one that owns that child.

* You get 5 rolls per 1h;
* You can claim a child to yourself once each 3 hours. 

use:
* `?waifu`  or `?w`: Will consume a roll point. If child doesn't have a owner, an emoticon will appear, first one that clicks on it and has a claim gets the child. (consuming the claim).

* `?waifulist [mention]` or `?wl [mention]`: Lists user claimed childs. If no mention is provided, list will load author list.

* `?waifuclaim` or `?wc`: Informs the time required to next claim reset and if you have a claim available.

* `?favoritewaifu <name>` or `?fw <name>`: Search the child that matches the name and add the thumbnail at your list.

* `?waifuinfo <name>` or `?wi` : Search the unit in the waifu game db.

* `waifutrade <mention>` or `?wt`: Trade your waifu with someone else.

* `waifurelease <name>` or `?wr <name>`: Release your unit.
