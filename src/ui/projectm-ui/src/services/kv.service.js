import { DefaultAzureCredential } from "@azure/identity";
import { SecretClient } from "@azure/keyvault-secrets";

const keyVaultUrl = "";
const credential = new DefaultAzureCredential();
const secretClient = new SecretClient(keyVaultUrl, credential);

export async function getSecret(secretName) {
  try {
    const secret = await secretClient.getSecret(secretName);
    return secret.value;
  } catch (error) {
    console.error("Error fetching secret:", error.message);
    return null;
  }
}