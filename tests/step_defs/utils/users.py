# user related utilities for the API test framework
import random


class UserNames(object):
    _base_user_name: str = "dougtest"

    @classmethod
    def generate_username(cls) -> str:
        # Generate a recognizable, but unique username.
        return cls._base_user_name + str(random.randint(10000, 99999))
