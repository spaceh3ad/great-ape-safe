from great_ape_safe import GreatApeSafe
import pytest


@pytest.fixture
def safe():
    return GreatApeSafe("dev.badgerdao.eth")


@pytest.fixture
def usdc(safe):
    return safe.contract("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


@pytest.fixture
def ausdc(safe):
    return safe.contract("0xBcca60bB61934080951369a648Fb03DF4F96263C")


def test_deposit(safe, usdc, ausdc):
    bal_before_usdc = usdc.balanceOf(safe)
    bal_before_ausdc = ausdc.balanceOf(safe)
    to_deposit = 100_000 * 10 ** usdc.decimals()

    safe.init_aave()
    safe.aave.deposit(usdc, to_deposit)

    assert usdc.balanceOf(safe) == bal_before_usdc - to_deposit
    assert ausdc.balanceOf(safe) == bal_before_ausdc + to_deposit


# def test_withdraw(safe):
