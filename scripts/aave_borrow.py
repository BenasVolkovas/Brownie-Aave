from brownie import network, config
from scripts.helpful_scripts import get_account, FORKED_LOCAL_ENVIRONMENTS
from scripts.get_weth import get_weth


def aave_borrow():
    account = get_account()
    erc20Address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        get_weth()


def main():
    aave_borrow()
