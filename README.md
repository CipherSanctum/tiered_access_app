# Tiered levels of access app for Django 2.x

### DESCRIPTION:

This is a base app / template to allow you to have tiered levels of access based
on whatever you want. Includes a helpful reminder to let the user know the result
of the last action they took *(updated, enabled, do this, do that, etc).*

#### Example:

If you had a *User* who signed up and paid you, you could give them level 1, 2, or 3
based on what they paid. Now all you have to do is fetch the model in your database
and give it to them in the dictionary of the view, and add the object to the template.
