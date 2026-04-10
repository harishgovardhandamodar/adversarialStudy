// Test file for transaction parser
import { TransactionParser } from '../src/data/transaction-parser';
import { Transaction, Account } from '../src/models/transaction';

describe('TransactionParser', () => {
  const sampleCSV = `
id,accountId,amount,currency,date,time,institution,description,category,location
1,ACC001,125.50,USD,2025-01-15,09:30,BankA,"Online Purchase","Shopping","Online"
2,ACC001,89.99,USD,2025-01-15,18:45,BankA,"Grocery Store","Food","Local"
3,ACC002,245.00,USD,2025-01-16,11:20,BankB,"Electronics Store","Shopping","Local"
`;

  const sampleJSON = [
    {
      id: "1",
      accountId: "ACC001",
      amount: 125.50,
      currency: "USD",
      date: "2025-01-15",
      time: "09:30",
      institution: "BankA",
      description: "Online Purchase",
      category: "Shopping",
      location: "Online"
    },
    {
      id: "2",
      accountId: "ACC001",
      amount: 89.99,
      currency: "USD",
      date: "2025-01-15",
      time: "18:45",
      institution: "BankA",
      description: "Grocery Store",
      category: "Food",
      location: "Local"
    }
  ];

  it('should parse CSV data correctly', () => {
    const transactions = TransactionParser.parseCSV(sampleCSV);
    
    expect(transactions).toHaveLength(2);
    expect(transactions[0].id).toBe('1');
    expect(transactions[0].accountId).toBe('ACC001');
    expect(transactions[0].amount).toBe(125.50);
    expect(transactions[0].institution).toBe('BankA');
  });

  it('should parse JSON data correctly', () => {
    const transactions = TransactionParser.parseJSON(sampleJSON);
    
    expect(transactions).toHaveLength(2);
    expect(transactions[0].id).toBe('1');
    expect(transactions[0].accountId).toBe('ACC001');
    expect(transactions[0].amount).toBe(125.50);
    expect(transactions[0].institution).toBe('BankA');
  });

  it('should group transactions by account', () => {
    const transactions = TransactionParser.parseCSV(sampleCSV);
    const accounts = TransactionParser.groupByAccount(transactions);
    
    expect(accounts).toHaveLength(2);
    expect(accounts[0].id).toBe('ACC001');
    expect(accounts[0].transactions).toHaveLength(2);
    expect(accounts[1].id).toBe('ACC002');
    expect(accounts[1].transactions).toHaveLength(1);
  });

  it('should handle empty data gracefully', () => {
    const emptyCSV = `
id,accountId,amount,currency,date,time,institution,description,category,location
`;
    
    const transactions = TransactionParser.parseCSV(emptyCSV);
    expect(transactions).toHaveLength(0);
  });
});

// Test file for privacy attack
import { PrivacyAttack } from '../src/attacks/privacy-attack';
import { TransactionParser } from '../src/data/transaction-parser';

describe('PrivacyAttack', () => {
  const sampleCSV = `
id,accountId,amount,currency,date,time,institution,description,category,location
1,ACC001,125.50,USD,2025-01-15,09:30,BankA,"Online Purchase","Shopping","Online"
2,ACC001,89.99,USD,2025-01-15,18:45,BankA,"Grocery Store","Food","Local"
3,ACC002,245.00,USD,2025-01-16,11:20,BankB,"Electronics Store","Shopping","Local"
4,ACC002,45.00,USD,2025-01-16,14:15,BankB,"Coffee Shop","Food","Local"
5,ACC003,75.25,USD,2025-01-17,10:10,BankC,"Restaurant","Food","Local"
`;

  it('should initialize correctly', () => {
    const attack = new PrivacyAttack();
    expect(attack.getName()).toBe('Privacy Attack');
    expect(attack.getStatus()).toBe(false);
  });

  it('should process transaction data without errors', async () => {
    const transactions = TransactionParser.parseCSV(sampleCSV);
    const accounts = TransactionParser.groupByAccount(transactions);
    
    const attack = new PrivacyAttack();
    attack.setTargetData(accounts);
    
    // Should not throw an error
    await expect(attack.start()).resolves.not.toThrow();
  });

  it('should calculate statistics correctly', () => {
    const attack = new PrivacyAttack();
    
    // Test mean calculation
    const mean = attack['calculateMean']([1, 2, 3, 4, 5]);
    expect(mean).toBe(3);
    
    // Test median calculation
    const median = attack['calculateMedian']([1, 2, 3, 4, 5]);
    expect(median).toBe(3);
    
    // Test standard deviation calculation
    const stdDev = attack['calculateStandardDeviation']([1, 2, 3, 4, 5]);
    expect(stdDev).toBeCloseTo(1.414, 3);
  });
});