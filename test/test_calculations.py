import pytest
from app.calculations import InsufficientFunds, add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount(0)

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [(3,2,5), (7,1,8),(12,4,16)])
def test_add(num1, num2, expected):
#    print("testing add function")
    assert add(num1,num2) == expected

def test_subtract():
    assert subtract(9,4) == 5

def test_multiply():
    assert multiply(9,4) == 36

def test_divide():
    assert divide(20,4) == 5    


def test_bank_set_inital_amount(bank_account):
    # bank_account = BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    print("testing my bank account")
    assert zero_bank_account.balance == 0

def test_deposit(bank_account):
    # bank_account = BankAccount()
    bank_account.deposit(50)
    assert bank_account.balance == 100

def test_withdraw(bank_account):
    # bank_account = BankAccount()
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_collect_interest(bank_account):
    # bank_account = BankAccount(100)
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [(200,100,100), (50,10,40),(1200,200,1000)])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    # tells pytest to expect an exception
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
