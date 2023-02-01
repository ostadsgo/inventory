from inventory import Product, ProductFile, User
import os

try:
    os.remove("./testshop.txt")
except Exception as e:
    print(e)
file = ProductFile("testshop.txt")


def test_product_save():
    p = Product("iphone", 2, 1350)
    p.productfile = file
    return p.save()


def test_product_is_exist(name):
    p = Product(name)
    p.productfile = file
    return p.is_exist()


def test_product_add(name):
    p = Product(name)
    p.productfile = file
    return p.add()


def test_product_remove(name):
    p = Product(name)
    p.productfile = file
    return p.remove()


def test_product_search(name):
    p = Product(name)
    p.productfile = file
    return p.search()


def test_user_check_passwd(username, passwd):
    user = User(username=username, password=passwd)
    return user.check_passwd()


def test_user_auth(username, password):
    user = User(username=username, password=password)
    return user.authorization()


def run_tests():
    i = 0
    assert test_product_save() == True
    print(f"✅ Test #{i} Passed. ::SAVE")
    i += 1
    # is exist
    assert test_product_is_exist("iphone") == 0
    print(f"✅ Test #{i} Passed. ::EXIST")
    i += 1
    assert test_product_is_exist("not exist") == -1
    print(f"✅ Test #{i} Passed. ::EXIST")
    i += 1
    # add
    assert test_product_add("iphone") == False
    print(f"✅ Test #{i} Passed.::ADD")
    i += 1
    assert test_product_add("dell xps") == True
    print(f"✅ Test #{i} Passed.::ADD")
    i += 1
    # remove
    assert test_product_remove("iphone") == True
    print(f"✅ Test #{i} Passed.::REMOVE")
    i += 1
    # search
    assert test_product_search("not exist") == ""
    print(f"✅ Test #{i} Passed.::SEARCH")
    i += 1
    ## USER
    # check user credentials.
    assert test_user_check_passwd("johndoe", "123e12s") == False
    print(f"✅ Test #{i} Passed.::CHECK_PASSWOD")
    i += 1
    assert test_user_check_passwd("admin", "123") == True
    print(f"✅ Test #{i} Passed.::CHECK_PASSWOD")
    i += 1
    assert test_user_check_passwd("admin", "123") == True
    print(f"✅ Test #{i} Passed.::AUTH")
    i += 1


if __name__ == "__main__":
    run_tests()
