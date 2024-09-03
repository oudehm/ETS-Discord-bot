This is a Discord bot designed to help manage a community server by automating roles, enforcing rules against profanity, and providing useful commands for members. 
The bot is built using discord.py and has several key features to streamline server management.

Features
Auto-Role Assignment:

  - Automatically assigns a role to new members upon joining the server.
  - Reacting to a specific message in the rules channel will assign the "Member" role and remove the "Unverified" role.

Profanity Filter:

  - Monitors messages for profanity using the better_profanity library.
  - Deletes messages containing profanity and notifies the user.
  - Tracks profanity violations per user.
  - Applies a "Timeout" role after multiple violations, with escalating actions at 3 and 5 violations.
  - Notifies server officers when a user reaches 5 violations.

Invite Tracking:

  - Tracks which invite link was used when a new member joins the server.
  - Automatically assigns a "Recruitment" role if a specific invite code is used.

Custom Commands:

  - !profanitycount: Displays the number of profanity violations for each user.
  - !socials: Shares the server's social media links.
  - !tutoring: Displays the tutoring schedule.
  - !contact: Provides contact information for server administrators.
