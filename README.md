# Discord.py bot with commands extension

Basic template for a discord bot with the commands extension and [cogs](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html)

### Pre-Setup

If you don't already have a discord bot, click [here](https://discordapp.com/developers/), accept any prompts then click "New Application" at the top right of the screen.  Enter the name of your bot then click accept.  Click on Bot from the panel from the left, then click "Add Bot."  When the prompt appears, click "Yes, do it!" 

### Setup

Create a file named `.env`

Add `DISCORD_BOT_SECRET=<your bot token>`

Your .env file should look something like this:

```
DISCORD_BOT_SECRET=<Bot token>
```

After adding your bot token to your .env file, navigate to line 10 in `main.py`. Change  `894969735207329893` to your user id. To get your id, ensure developer mode is enabled (Settings->Appearance->Advanced->Developer Mode) then right-click on yourself and click copy id.

When you hit start everything should startup fine.
