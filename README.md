# Tiered levels of access app for Django 2.x

### DESCRIPTION:

This is a base app / template to allow you to have tiered levels of access based
on whatever you want. Includes a helpful reminder to let the user know the result
of the last action they took *(updated, enabled, do this, do that, etc).*

### EXAMPLE:

Can be found here once you signup and login:  https://pwnsaucedesigns.com/tiered_access_app/

It only demonstrates the principle. Notice the url upon activating a level is always the same.

A realistic example would be if you had a *User* who signed up and paid you, you could give them level
1, 2, or 3 based on what they paid. Now all you have to do is fetch the model in your database and give
it to them in the dictionary for that particular level, add the object(s) to the template, and loop/filter if required.
