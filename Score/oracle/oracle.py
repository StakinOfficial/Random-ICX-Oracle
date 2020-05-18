from iconservice import *

TAG = 'RandomOracle'

# An interface of system score
class RandomOracle(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self.admin_address = VarDB('admin_address', db, value_type=Address)
        self.expiry = VarDB('expiry', db, value_type=int)
        self.increase = VarDB('increase', db, value_type=int)
        self.random = VarDB('random', db, value_type=int)

    def on_install(self) -> None:
        super().on_install()
        self.admin_address.set(self.msg.sender)
        self.expiry.set(self.now())
        self.increase.set(1800000000) # 30 minutes
        
    def on_update(self) -> None:
        super().on_update()

    @external
    def setIncrease(self, value: int):
        if msg.sender != admin_address:
            revert("only admin can change timer")
        self.increase.set(value)
    
    @external
    def setRandom(self, value: int):
        if self.msg.sender != self.admin_address.get():
            revert("only admin can commit a random number")
        if value < 0 or value > 100000: 
            revert("only values between 0 and 100000 is allowed")
#        if self.now() < self.expiry.get() :
#            revert("previous random number is still valid")
        self.random.set(value)
        self.expiry.set(self.now() + self.increase.get())

    @external(readonly=True)
    def getRandom(self) -> int:
    	return self.random.get()
