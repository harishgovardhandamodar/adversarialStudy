// Transaction data model for bank transaction data
export interface Transaction {
  id: string;
  accountId: string;
  amount: number;
  currency: string;
  date: string;
  time: string;
  institution: string;
  description: string;
  category: string;
  location: string;
}

export interface Account {
  id: string;
  institution: string;
  accountNumber: string;
  transactions: Transaction[];
  balance: number;
}