import { Transaction, Account } from '../models/transaction';
export declare class TransactionParser {
    /**
     * Parse transaction data from CSV or JSON format
     */
    static parseTransactionData(data: string | any[]): Transaction[];
    /**
     * Parse CSV formatted transaction data
     */
    static parseCSV(csvData: string): Transaction[];
    /**
     * Parse JSON formatted transaction data
     */
    static parseJSON(jsonData: any[]): Transaction[];
    /**
     * Group transactions by account
     */
    static groupByAccount(transactions: Transaction[]): Account[];
}
