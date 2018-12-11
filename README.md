After creating a virtual env and installing the `requirements.txt` packages:

`(virtualenv)$ pytest`

The tests located in `user/test_user.py` will save a `UserChangeForm` with `'is_superuser' = True` and test if the superuser is added to the group `Superuser`.

The above is achieved by catching a `post_save` signal of the `User` model in `user.signals.py`.

The tests provided show that the necessary conditions for a successfull result are:
* The save call to be in a `transaction.atomic()` 
* The use of [transaction.on_commit()](https://docs.djangoproject.com/en/dev/topics/db/transactions/#django.db.transaction.on_commit). 

Without either of those, the user will not be added to any groups.
