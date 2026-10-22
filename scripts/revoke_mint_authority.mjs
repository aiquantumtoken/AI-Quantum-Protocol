import {
  Connection,
  Keypair,
  PublicKey,
  clusterApiUrl,
  sendAndConfirmTransaction,
  Transaction
} from '@solana/web3.js';
import {
  AuthorityType,
  createSetAuthorityInstruction,
  TOKEN_2022_PROGRAM_ID
} from '@solana/spl-token';
import fs from 'fs';

async function revokeMint() {
  const connection = new Connection(clusterApiUrl('devnet'), 'confirmed');
  const rawKey = JSON.parse(fs.readFileSync('deployer_keypair.json', 'utf-8'));
  const payer = Keypair.fromSecretKey(Uint8Array.from(rawKey));

  const mint = new PublicKey('FfMfS6WARfZWS1ytMqTBiwsJzPUJnRpKNpPqrWoAcaGa');

  console.log("Revoking Mint Authority for $AIQT...");
  const tx = new Transaction().add(
    createSetAuthorityInstruction(
      mint,
      payer.publicKey,
      AuthorityType.MintTokens,
      null, // Revoke permanently
      [],
      TOKEN_2022_PROGRAM_ID
    )
  );

  const sig = await sendAndConfirmTransaction(connection, tx, [payer]);
  console.log(`✅ Mint Authority Revoked Permanently! Tx: ${sig}`);
}

revokeMint().catch(console.error);
