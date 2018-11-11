
import os
import hashlib
import random
from datetime import datetime
from mapex import EntityModel, CollectionModel, SqlMapper, Pool, MySqlClient
from exceptions import AlreadyRegistred, IncorrectPassword, IncorrectLogin, IncorrectToken


# define connection pool for database:
pool = Pool(
    MySqlClient,
    (
        os.environ.get("MYSQL_HOST"),
        os.environ.get("MYSQL_PORT"),
        os.environ.get("MYSQL_USER"),
        os.environ.get("MYSQL_PASS"),
        os.environ.get("MYSQL_DBNAME")
    )
)


class CredentialsMapper(SqlMapper):
    """ describes relations between py-models and database structure """
    pool = pool

    def bind(self):
        self.set_new_item(CredentialsRecord)
        self.set_new_collection(CredentialsRecords)
        self.set_collection_name("credentials")
        self.set_map([
            self.str("login", "Login"),
            self.str("password", "Password"),
            self.str("token", "Token"),
            self.datetime("created", "Created"),
        ])
        self.set_primary("login")


class CredentialsRecord(EntityModel):
    """ represents single record from table `auth` """
    mapper = CredentialsMapper

    def describe(self):
        return self.stringify(["login", "password", "token"])


class CredentialsRecords(CollectionModel):
    """ represents all the records from table `auth` """
    mapper = CredentialsMapper

    @staticmethod
    def create_new(login: str, password: str) -> bool:
        """ creating new account with given login and password """
        with CredentialsRecords.mapper.pool.transaction:
            if CredentialsRecords().count({"login": login}):
                raise AlreadyRegistred()
            else:
                CredentialsRecord({
                    "login": login,
                    "password": md5(password),
                    "token": gen_token(),
                    "created": datetime.now()
                }).save()
        return True

    @staticmethod
    def auth(login: str, password: str) -> str:
        """ authenticating with login and password """
        with CredentialsRecords.mapper.pool.transaction:
            match = CredentialsRecords().get_item({"login": login})
            if match and match.password == md5(password):
                match.token = gen_token()
                match.save()
                return match.token
            elif match:
                raise IncorrectPassword()
            else:
                raise IncorrectLogin()

    @staticmethod
    def auth_by_token(token: str) -> bool:
        """ authenticating with token """
        match = CredentialsRecords().get_item({"token": token})
        if match:
            return match.login
        else:
            raise IncorrectToken()


def md5(value) -> str:
    """ md5 """
    if not isinstance(value, bytes):
        value = str(value).encode()
    return hashlib.md5(value).hexdigest()

def gen_password() -> str:
    """ Generating password """
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    characters = ["a", "b", "d", "e", "f", "g", "h", "j", "k", "m", "n",
                  "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]
    digit1 = str(random.choice(digits))
    digit2 = str(random.choice(digits))
    upper_char = random.choice(characters).upper()
    random.shuffle(characters)
    random_start = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
    random_end = random_start + 5
    chars = characters[random_start:random_end]
    l = [digit1, digit2, upper_char] + chars
    random.shuffle(l)
    return "".join(l)

def gen_token() -> str:
    """ Generating token """
    return md5("%s%d" % (str(datetime.now()), random.choice(range(100))))