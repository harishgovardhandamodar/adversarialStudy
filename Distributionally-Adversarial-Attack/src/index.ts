// Test file for privacy attack implementation
import { TransactionParser } from './data/transaction-parser';
import { PrivacyAttack } from './attacks/privacy-attack';

// Sample transaction data
const sampleData = `
id,accountId,amount,currency,date,time,institution,description,category,location
1,ACC001,125.50,USD,2025-01-15,09:30,BankA,"Online Purchase","Shopping","Online"
2,ACC001,89.99,USD,2025-01-15,18:45,BankA,"Grocery Store","Food","Local"
3,ACC002,245.00,USD,2025-01-16,11:20,BankB,"Electronics Store","Shopping","Local"
4,ACC002,45.00,USD,2025-01-16,14:15,BankB,"Coffee Shop","Food","Local"
5,ACC003,75.25,USD,2025-01-17,10:10,BankC,"Restaurant","Food","Local"
6,ACC003,300.00,USD,2025-01-17,19:30,BankC,"Movie Tickets","Entertainment","Local"
7,ACC001,150.00,USD,2025-01-18,08:00,BankA,"Gas Station","Transport","Local"
8,ACC002,67.50,USD,2025-01-18,17:45,BankB,"Online Purchase","Shopping","Online"
9,ACC003,22.99,USD,2025-01-19,12:30,BankC,"Book Store","Education","Local"
10,ACC001,99.99,USD,2025-01-19,20:15,BankA,"Restaurant","Food","Local"
`;

async function runAttack() {
  console.log("Initializing privacy attack on transaction data...\n");
  
  // Parse transaction data
  const transactions = TransactionParser.parseCSV(sampleData);
  console.log("Parsed transactions:", transactions.length);
  
  // Group by account
  const accounts = TransactionParser.groupByAccount(transactions);
  console.log("Grouped into accounts:", accounts.length);
  
  // Run privacy attack
  const attack = new PrivacyAttack();
  attack.setTargetData(accounts);
  await attack.start();
  
  console.log("\nPrivacy attack completed successfully!");
}

// Run the attack
runAttack().catch(console.error);