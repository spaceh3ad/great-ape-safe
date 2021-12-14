from brownie_tokens.forked import MintableForkToken
import pytest
from conftest import native, aave, safe
from scripts.mint import mint
from brownie import exceptions
from brownie_tokens.forked import MintableForkToken


@pytest.mark.parametrize("native_asset, aave_asset", zip(native, aave), indirect=True)
def test_deposits(safe, native_asset, aave_asset):
    _native_asset = safe.contract(native[native_asset].upper())
    _aave_asset = safe.contract(aave[aave_asset].upper())

    bal_before_native_asset_deposit = _native_asset.balanceOf(safe)
    bal_before_aave_asset_deposit = _aave_asset.balanceOf(safe)
    to_deposit = 100 * 10 ** _native_asset.decimals()

    safe.init_aave()

    # if not enough native assets -> revert
    # if bal_before_native_asset_deposit < to_deposit:
    #     mint(
    #         MintableForkToken._mint_for_testing(
    #             safe,
    #         )
    #     )

    safe.aave.deposit(_native_asset, to_deposit)
    assert _native_asset.balanceOf(safe) == bal_before_native_asset_deposit - to_deposit
    assert _aave_asset.balanceOf(safe) == bal_before_aave_asset_deposit + to_deposit


# def test_withdraw(safe, usdc, ausdc):
#     safe.aave.withdraw(usdc, 100_000 * 10 ** usdc.decimals())
