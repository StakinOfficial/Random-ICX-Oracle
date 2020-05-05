from iconservice import *

TAG = 'RandomOracle'

# An interface of system score
class RandomOracle(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self.admin_address = VarDB('admin_address', db, value_type=Address)

    def on_install(self, _addr_admin: Address) -> None:
        super().on_install()
        self.admin_address.set(self.msg.sender)
        
    def on_update(self) -> None:
        super().on_update()

    @external
    def setRandom(self, value: int):
        if msg.sender != admin_address:
            revert("only admin can commit a random number")
        if value < 0 or value > 1: 
            revert("only values between 0 and 1 is allowed")
        self.random.set(value)

    @external(readonly=True)
    def getRandom() -> int:
        return self.random.get()
