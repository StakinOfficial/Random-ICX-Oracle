import IconService, { IconAmount, IconConverter, HttpProvider, IconWallet, IconBuilder} from 'icon-sdk-js';

const config = {
    adminPk : "<PRIVATE_KEY>",
    scoreAddr : "<CONTRACT_ADDRESS>",
    iconAPI : "https://bicon.net.solidwallet.io/api/v3"
}

const provider = new HttpProvider(config.iconAPI);
const iconService = new IconService(provider);

// Admin wallet
const adminWallet = IconWallet.loadPrivateKey(config.adminPk);

function setRandom() {
    // Build transaction
    const { CallTransactionBuilder } = IconBuilder;
    const txObj = new CallTransactionBuilder()
        .from(adminWallet.getAddress())
        .to(config.scoreAddr)
        .stepLimit(IconConverter.toBigNumber('2000000'))
        // .nid(IconConverter.toBigNumber('3')) 
        // .nonce(IconConverter.toBigNumber('1'))
        // .version(IconConverter.toBigNumber('3'))
        .value(IconAmount.of(0, IconAmount.Unit.ICX).toLoop())
        // .timestamp((new Date()).getTime() * 1000)
        .method('setRandom')
        .params({
            value: Math.random()
        })
        .build()

    // Sign & send tx 🥳
    const signedTransaction = new SignedTransaction(txObj, adminWallet)
    const txHash = await iconService.sendTransaction(signedTransaction).execute();
    console.log(txHash)
}


// Run every 30 minutes
setInterval(setRandom, 1800000);