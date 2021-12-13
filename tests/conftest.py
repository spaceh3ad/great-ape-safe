import pytest
from great_ape_safe import GreatApeSafe

aave = {
    "aUSDC": "0xBcca60bB61934080951369a648Fb03DF4F96263C",
    "aDAI": "0x028171bca77440897b824ca71d1c56cac55b68a3",
    "aAAVE": "0xFFC97d72E13E01096502Cb8Eb52dEe56f74DAD7B",
    "aUSDT": "0x3ed3b47dd13ec9a98b44e6204a523e766b225811",
    "aZRX": "0xdf7ff54aacacbff42dfe29dd6144a69b629f8c9e",
    "aWETH": "0x030ba81f1c18d280636f32af80b9aad02cf0854e",
    "aSUSD": "0x6c5024cd4f8a59110119c56f8933403a539555eb",
    "aTUSD": "0x101cc05f4a51c0319f570d5e146a8c625198e636",
    "aMKR": "0xc713e5e149d5d0715dcd1c156a020976e7e56b88",
    "aWBTC": "0x9ff58f4ffb29fa2266ab25e75e2a8b3503311656",
    "aUNI": "0xb9d7cb55f463405cdfbe4e90a6d2df01c2b92bf1",
    "aYFI": "0x5165d24277cd063f5ac44efd447b27025e888f37",
    "aBUSD": "0xa361718326c15715591c299427c62086f69923d9",
    "aMANA": "0xa685a61171bb30d4072b338c80cb7b2c865c873e",
    "aSNX": "0x35f6b052c598d933d69a4eec4d04c73a191fe6c2",
    "aBAT": "0x05ec93c0365baaeabf7aeffb0972ea7ecdd39cf1",
    "aENJ": "0xac6df26a590f08dcc95d5a4705ae8abbc88509ef",
}

native = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "AAVE": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "ZRX": "0xE41d2489571d322189246DaFA5ebDe1F4699F498",
    "WETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    # "GUSD": "0x056fd409e1d7a124bd7017459dfea2f387b6d5cd",
    "SUDS": "0x57ab1ec28d129707052df4df418d58a2d46d5f51",
    "TrueUSD": "0x0000000000085d4780B73119b644AE5ecd22b376",
    # "USDP": "0x8e870d67f660d95d5be530380d0ec0bd388289e1",
    "MKR": "0x0f51bb10119727a7e5eA3538074fb341F56B09Ad",
    "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
    "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    # "SUSHI": "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2",
    "YFI": "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",
    "BUSD": "0x4fabb145d64652a948d72533023f6e7a623c7c53",
    "MANA": "0x0F5D2fB29fb7d3CFeE444a200298f468908cC942",
    "SNX": "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F",
    "BAT": "0x0d8775f648430679a709e98d2b0cb6250d2887ef",
    "ENJ": "0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c",
    # "CRV": "0xD533a949740bb3306d119CC777fa900bA034cd52",
}


@pytest.fixture(params=aave.items())
def aave_asset(request):
    return request.param


@pytest.fixture(params=native.items())
def native_asset(request):
    return request.param


@pytest.fixture
def safe():
    safe = GreatApeSafe("dev.badgerdao.eth")
    return safe
