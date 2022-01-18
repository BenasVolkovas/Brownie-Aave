from brownie import interface, network, config
from scripts.helpful_scripts import get_account, FORKED_LOCAL_ENVIRONMENTS
from scripts.get_weth import get_weth
from web3 import Web3

AMOUNT = Web3.toWei(0.1, "ether")


def approve_erc20(amount, spender, erc20Address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20Address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_lending_pool():
    lendingPoolAddressesProvider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )

    lendingPoolAddress = lendingPoolAddressesProvider.getLendingPool()
    lendingPool = interface.ILendingPool(lendingPoolAddress)

    return lendingPool


def get_borrow_data(lendingPool, account):
    (
        totalCollateralEth,
        totalDebtEth,
        availableBorrowEth,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    ) = lendingPool.getUserAccountData(account.address)
    availableBorrowEth = Web3.fromWei(availableBorrowEth, "ether")
    totalCollateralEth = Web3.fromWei(totalCollateralEth, "ether")
    totalDebtEth = Web3.fromWei(totalDebtEth, "ether")
    print(f"You have {totalCollateralEth} worth of ETH deposited.")
    print(f"You have {totalDebtEth} worth of ETH borrowed.")
    print(f"You cam borrow {availableBorrowEth} worth of ETH.")
    return (float(availableBorrowEth), float(totalDebtEth))


def get_asset_price(price_feed_address):
    pass


def aave_borrow():
    account = get_account()
    erc20Address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        get_weth()
    lendingPool = get_lending_pool()

    approve_erc20(AMOUNT, lendingPool.address, erc20Address, account)
    print("Depositing...")
    tx = lendingPool.deposit(
        erc20Address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")

    borrowableEth, totalDebt = get_borrow_data(lendingPool, account)
    daiEthPrice = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )


def main():
    aave_borrow()
