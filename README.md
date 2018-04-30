# Kirinus Rewrite

Destiny child stuff related bot based using discord.py rewrite API wrapper.

Version 1.0 Kirinus Migrated to Discord.py Rewrite API!

Here is a overview of Kirinus Functions.

## New Features!
    * raid pics updated! Fancy raid pics on raid command

## Commands

Learn more about Kirinus commands:

* [Raid](#raid-command)
* [World Boss](#world-boss-command) (beta)
* [Quotes](#quote-command)
* [Reset](#reset-countdown)
* [Maint](#maint)
* Fun stuff

### Reset Countdown
Gives the countdown till the next reset.

Use:
`?reset`

![simple reset example](https://cdn.discordapp.com/attachments/242845451739463681/440325135749349377/unknown.png)

### Maint

Says when maint will start/started.

Use: `?maint`

updating maint time (for mods):
`?maint add "MM/DD hh:mm"`
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

**Important:** The raid name is the only argument that have a position fixed and must be the 2nd argument if you want to add other arguments.

#### Adding mention [raid owner] field:

Suppose that u found another person raid, how do you set the owner? Simple, just mention him on the command and Kirinus will do all the hard work.

`?raid nicole @MathBot#7353`

will tell me that the user Math found the raid:

![raid owner img](https://rodizipa.gitbooks.io/kirinus-docs/content/assets/Screenshot_2.png)

**Obs:**The reason i don't keep the mention on the box is because currently on mobile discord, mentions don't appear on embed boxes, instead the user id is displayed. That means that instead of the mention, mobile users will only see numbers. So, using the display name works for now.

#### Adding level field:

Kirinus will try to find numbers on the command line and return it as the raid level.

`?raid santa @MathBot#7353 12` OR `?raid santa 12 @MathBot#7353`

gives back:

![lvl field img](https://rodizipa.gitbooks.io/kirinus-docs/content/assets/Screenshot_3.png)


### World Boss Command

This command makes the reset call automatic, so you don't have to bother.

`?wb start/stop`

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

**Obs**: Kirinus can't replace existing tags. (For now.)