# Flask Feedback
## Tor Kingdon
### Springboard Software Engeineering Career Track sub-sub-unit 24.4.20

## Authentication and Authorization exercise
### Uses Bcrypt, SQLAlchemy, Postgresql, Flask-WTForms... see requirements.txt for details

## Steps to the assignment:
 1. User Model
 2. Base Template
 3. Users Routes
 4. Make /secret, you know, secret
 5. Log out
 6. Make /users/<username>
 7. Feedback Model
 8. Feedback Routes (also modify user routes)

## What that means to the user:
 - Registered users can login or new users can register. 
 - There is content for users only, including user profiles for any user. 
 - Users can post feedback.
 - All users can view feedback no matter who wrote it.
 - Users can edit or delete their own feedback only.
 - Users can delete themselves, which will delete all of their feedback as well.

## Future development ideas
 - user delete could use a confirmation warning
   - I started one that's like github's where the user has to type their own username in after clicking delete
   - could also just do an alert, or whatever the alerts are that you can cancel
 - admin user (boolean column in user db 'is_admin') can edit or delete everyone's feedback
 - admin replies to feedback?