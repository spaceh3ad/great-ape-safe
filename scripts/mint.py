from brownie_tokens.forked import MintableForkToken
from brownie import Contract


def mint(token: MintableForkToken, target: str, amount: int, address: str) -> None:
    if not hasattr(token, "UNDERLYING_ASSET_ADDRESS"):
        return False

    token = MintableForkToken(token.UNDERLYING_ASSET_ADDRESS())
    lending_pool = Contract(address)
    token._mint_for_testing(target, amount)
    token.approve(lending_pool, amount, {"from": target})
    lending_pool.deposit(token, amount, target, 0, {"from": target})
    return True
