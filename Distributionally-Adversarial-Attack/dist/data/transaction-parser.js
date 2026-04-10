"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TransactionParser = void 0;
class TransactionParser {
    /**
     * Parse transaction data from CSV or JSON format
     */
    static parseTransactionData(data) {
        if (typeof data === 'string') {
            // Handle CSV parsing
            return this.parseCSV(data);
        }
        else {
            // Handle JSON array parsing
            return this.parseJSON(data);
        }
    }
    /**
     * Parse CSV formatted transaction data
     */
    static parseCSV(csvData) {
        const lines = csvData.trim().split('\n');
        const headers = lines[0].split(',').map(header => header.trim());
        return lines.slice(1).map((line) => {
            const values = line.split(',');
            return {
                id: values[0],
                accountId: values[1],
                amount: parseFloat(values[2]),
                currency: values[3],
                date: values[4],
                time: values[5],
                institution: values[6],
                description: values[7],
                category: values[8],
                location: values[9]
            };
        });
    }
    /**
     * Parse JSON formatted transaction data
     */
    static parseJSON(jsonData) {
        return jsonData.map(item => ({
            id: item.id,
            accountId: item.accountId,
            amount: item.amount,
            currency: item.currency,
            date: item.date,
            time: item.time,
            institution: item.institution,
            description: item.description,
            category: item.category,
            location: item.location
        }));
    }
    /**
     * Group transactions by account
     */
    static groupByAccount(transactions) {
        const accounts = {};
        transactions.forEach(transaction => {
            if (!accounts[transaction.accountId]) {
                accounts[transaction.accountId] = {
                    id: transaction.accountId,
                    institution: transaction.institution,
                    accountNumber: transaction.accountId.substring(0, 8), // Simplified
                    transactions: [],
                    balance: 0
                };
            }
            accounts[transaction.accountId].transactions.push(transaction);
        });
        // Calculate balances (simplified)
        Object.values(accounts).forEach(account => {
            account.balance = account.transactions.reduce((sum, t) => sum + t.amount, 0);
        });
        return Object.values(accounts);
    }
}
exports.TransactionParser = TransactionParser;
