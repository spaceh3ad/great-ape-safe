import pytest
from conftest import native, aave, safe


@pytest.mark.parametrize(
    "native_asset, aave_asset", zip(native.items(), aave.items()), indirect=True
)
def test_deposits(safe, native_asset, aave_asset):
    _native_asset = safe.contract(native_asset[1])
    _aave_asset = safe.contract(aave_asset[1])

    print(f"Testing for {native_asset[0]}/{aave_asset[0]}")
    bal_before_native_asset_deposit = _native_asset.balanceOf(safe)
    bal_before_aave_asset_deposit = _aave_asset.balanceOf(safe)
    print(f"{native_asset[0]}:{_native_asset.decimals()}")
    to_deposit = 100_000 * 10 ** _native_asset.decimals()

    safe.init_aave()
    safe.aave.deposit(_native_asset, to_deposit)

    assert _native_asset.balanceOf(safe) == bal_before_native_asset_deposit - to_deposit
    assert _aave_asset.balanceOf(safe) == bal_before_aave_asset_deposit + to_deposit


# def test_withdraw(safe, usdc, ausdc):
#     safe.aave.withdraw(usdc, 100_000 * 10 ** usdc.decimals())
