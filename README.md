t# scratchrequest
 _A package for communicating with scratch.mit.edu's cloud variables, getting/setting userdata, projects and studios!_

**For most of the features you need a [Scratch](https://scratch.mit.edu/) account. You can signup for free at [https://scratch.mit.edu/](https://scratch.mit.edu/).**

# Installation

To install this library, just type ```pip install scratchrequest``` in the terminal (Command Prompt)

*****OR*****

Run this Python program

```python
import os

os.system('pip install scratchrequest')
```

**If you still have troubles while installing then go
to [this link](https://packaging.python.org/tutorials/installing-packages/)**

# Logging in

*Login with username and password:*


Following is a simple program to make a simple connection:

```python
import scratchrequest

session = scratchrequest.Login(username="Your_Username", password="Your_Password")
```

It will give an error if the `username` or `password` is invalid.




*Login with sessionId cookie:*

Following is a simple program to make a connection with your cookies:

```python
import scratchrequest

session = scratchrequest.Session("Your_SessionID", username="Your_Username")
```

It will give an error if the `username` or `sessionID` is invalid or outdated.

# Managing user settings

With scratchrequest, you can easy edit some settings of your scratchaccount. The following program shows how.

```python
import scratchrequest

session = scratchrequest.Login(username="Your_Username", password="Your_Password")
settings = session.ManageSettings()

#Examples:
settings.check_password('Password') #Controls of the given password is correct
settings.change_country('Belgium') #Sets the country
settings.change_password(old_password='old password', new_passwod='new password')

Here i need to add some stuff, but i'm to lazy ...
```

# Connecting To Projects

You can easy get projectstats, and edit the settings.
To connect, use:

```python
import scratchrequest

session = scratchrequest.Login(username="Your_Username", password="Your_Password")
projects = session.ConnectProject(id=ProjectID)
```
**Or without session (Some features won't work!):**
```python
import scratchrequest

project = scratchrequest.get_project(id=ProjectID)
```

# Getting project stats:
