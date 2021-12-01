import pytest
from brownie import chain
from brownie.exceptions import VirtualMachineError
from brownie_tokens import MintableForkToken

from great_ape_safe import GreatApeSafe


# assumption: based on the convex dev docs it appears it is possible to
# claim rewards for another address, see quote below:
#
# > Use baseRewardPool.getReward() or baseRewardPool.getReward( address, bool )
# > to claim rewards for your address or an arbitrary address.
# https://docs.convexfinance.com/convexfinanceintegration/baserewardpool#claim-rewards
#
# test this by doing the following:
#
# set up fixture (build state from which other tests are ran):
# - build cvx_* position in first wallet (tops)
# - stakeFor it for a second wallet (tvault) (should transfer ownership)
#
# then test separately:
# - confirm ownership is lost; tops should not be able to unstake
# - confirm vault can unstake and thus is owner
# - confirm vault can claim rewards (to be expected)
# - confirm ops can claim rewards on behalf of the vault (real test!)


@pytest.fixture
def build_position(scope='module'):
    tops = GreatApeSafe('0x042B32Ac6b453485e357938bdC38e0340d4b9276')
    tvault = GreatApeSafe('0xD0A7A8B98957b9CD3cFB9c0425AbE44551158e9e')

    rencrv = tops.contract('0x49849C98ae39Fff122806C06791Fa73784FB3675')

    tops.init_curve()
    tops.init_convex()

    # mint wbtc
    wbtc = MintableForkToken('0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599')
    wbtc_amount = 1 * 10**wbtc.decimals()
    wbtc._mint_for_testing(tops, wbtc_amount)

    # build cvx position; wbtc -> rencrv -> cvx_rencrv
    tops.curve.deposit(rencrv, wbtc_amount, wbtc)
    tops.convex.deposit_all(rencrv)

    # stakeFor tvault
    tops.convex.stake(rencrv, wbtc_amount, tvault)


def test_tops_lost_ownership(build_position):
    # confirm tops cannot unstake
    tops = GreatApeSafe('0x042B32Ac6b453485e357938bdC38e0340d4b9276')
    tops.init_convex()

    rencrv = tops.contract('0x49849C98ae39Fff122806C06791Fa73784FB3675')

    with pytest.raises(VirtualMachineError):
        tops.convex.unstake_all(rencrv)


def test_vault_is_owner(build_position):
    # confirm tvault can unstake
    tvault = GreatApeSafe('0xD0A7A8B98957b9CD3cFB9c0425AbE44551158e9e')
    tvault.init_convex()

    rencrv = tvault.contract('0x49849C98ae39Fff122806C06791Fa73784FB3675')

    tvault.convex.unstake_all(rencrv)


def test_claim_from_owner(build_position):
    # confirm tvault can claim
    tops = GreatApeSafe('0x042B32Ac6b453485e357938bdC38e0340d4b9276')
    tvault = GreatApeSafe('0xD0A7A8B98957b9CD3cFB9c0425AbE44551158e9e')

    cvx = tvault.contract('0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B')

    tvault.init_convex()

    chain.mine(100)

    bal_before = cvx.balanceOf(tvault)
    tvault.convex.claim_all()
    assert cvx.balanceOf(tvault) > bal_before


def test_claim_on_behalf_of(build_position):
    # confirm ops can claim on behalf of
    tops = GreatApeSafe('0x042B32Ac6b453485e357938bdC38e0340d4b9276')
    tvault = GreatApeSafe('0xD0A7A8B98957b9CD3cFB9c0425AbE44551158e9e')

    rencrv = tops.contract('0x49849C98ae39Fff122806C06791Fa73784FB3675')
    cvx = tops.contract('0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B')

    tops.init_convex()

    chain.mine(100)

    _, _, _, rewards = tops.convex.get_pool_info(rencrv)
    bal_before = cvx.balanceOf(tops)
    tops.contract(rewards).getReward(tvault, 1)
    assert cvx.balanceOf(tops) > bal_before
