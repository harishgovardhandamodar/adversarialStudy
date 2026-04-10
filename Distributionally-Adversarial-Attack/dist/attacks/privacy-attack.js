"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PrivacyAttack = void 0;
// Privacy attack implementation using distributional analysis
const attack_framework_1 = require("./attack-framework");
class PrivacyAttack extends attack_framework_1.AttackFramework {
    constructor() {
        super('Privacy Attack');
        this.analysisResults = {};
    }
    /**
     * Execute privacy attack using distributional analysis
     */
    async execute() {
        console.log('Executing privacy attack using distributional analysis...');
        if (!this.targetData || this.targetData.length === 0) {
            throw new Error('No target data for privacy attack');
        }
        // Perform distributional analysis
        this.analysisResults = await this.performDistributionalAnalysis();
        // Extract patterns from transactions
        const patterns = this.extractPatterns();
        // Report findings (without exposing raw data)
        this.reportFindings(patterns);
    }
    /**
     * Perform distributional analysis on transaction data
     */
    async performDistributionalAnalysis() {
        // Group by account to get distribution patterns
        const accounts = this.targetData;
        const transactionCounts = [];
        const amountSums = [];
        const timeDistributions = {};
        const categoryDistributions = {};
        accounts.forEach(account => {
            transactionCounts.push(account.transactions.length);
            amountSums.push(account.balance);
            // Analyze time distribution
            account.transactions.forEach(transaction => {
                const time = transaction.time;
                if (!timeDistributions[time]) {
                    timeDistributions[time] = 0;
                }
                timeDistributions[time]++;
            });
            // Analyze category distribution
            account.transactions.forEach(transaction => {
                const category = transaction.category;
                if (!categoryDistributions[category]) {
                    categoryDistributions[category] = 0;
                }
                categoryDistributions[category]++;
            });
        });
        // Calculate statistical measures
        const stats = {
            transactionCount: {
                mean: this.calculateMean(transactionCounts),
                median: this.calculateMedian(transactionCounts),
                stdDev: this.calculateStandardDeviation(transactionCounts)
            },
            amountSum: {
                mean: this.calculateMean(amountSums),
                median: this.calculateMedian(amountSums),
                stdDev: this.calculateStandardDeviation(amountSums)
            },
            timeDistribution: timeDistributions,
            categoryDistribution: categoryDistributions
        };
        return stats;
    }
    /**
     * Extract patterns from distributional analysis
     */
    extractPatterns() {
        const accountData = this.targetData;
        const patterns = {
            suspiciousActivity: [],
            commonSpendingPatterns: [],
            accountSimilarities: []
        };
        // Find accounts with similar transaction patterns
        for (let i = 0; i < accountData.length; i++) {
            for (let j = i + 1; j < accountData.length; j++) {
                const account1 = accountData[i];
                const account2 = accountData[j];
                // Simple similarity check based on transaction counts and amounts
                const similarity = this.calculateAccountSimilarity(account1, account2);
                if (similarity > 0.8) {
                    patterns.accountSimilarities.push({
                        account1: account1.id,
                        account2: account2.id,
                        similarity: similarity
                    });
                }
            }
        }
        return patterns;
    }
    /**
     * Calculate account similarity based on transaction behavior
     */
    calculateAccountSimilarity(account1, account2) {
        // Compare transaction counts
        const countSimilarity = 1 - Math.abs(account1.transactions.length - account2.transactions.length) /
            Math.max(account1.transactions.length, account2.transactions.length);
        // Compare amount sums
        const sumSimilarity = 1 - Math.abs(account1.balance - account2.balance) /
            Math.max(account1.balance, account2.balance);
        // Weighted average (transaction count more important)
        return (countSimilarity * 0.7) + (sumSimilarity * 0.3);
    }
    /**
     * Calculate mean value
     */
    calculateMean(values) {
        if (values.length === 0)
            return 0;
        const sum = values.reduce((a, b) => a + b, 0);
        return sum / values.length;
    }
    /**
     * Calculate median value
     */
    calculateMedian(values) {
        if (values.length === 0)
            return 0;
        const sorted = [...values].sort((a, b) => a - b);
        const middle = Math.floor(sorted.length / 2);
        if (sorted.length % 2 === 0) {
            return (sorted[middle - 1] + sorted[middle]) / 2;
        }
        else {
            return sorted[middle];
        }
    }
    /**
     * Calculate standard deviation
     */
    calculateStandardDeviation(values) {
        if (values.length === 0)
            return 0;
        const mean = this.calculateMean(values);
        const squaredDifferences = values.map(value => Math.pow(value - mean, 2));
        const variance = this.calculateMean(squaredDifferences);
        return Math.sqrt(variance);
    }
    /**
     * Report findings without exposing raw sensitive data
     */
    reportFindings(patterns) {
        console.log('Privacy Attack Findings:');
        console.log('========================');
        // Report statistical patterns
        console.log(`Transaction Count Analysis:`);
        console.log(`  Mean: ${this.analysisResults.transactionCount.mean.toFixed(2)}`);
        console.log(`  Median: ${this.analysisResults.transactionCount.median.toFixed(2)}`);
        console.log(`  Standard Deviation: ${this.analysisResults.transactionCount.stdDev.toFixed(2)}`);
        console.log(`Amount Sum Analysis:`);
        console.log(`  Mean: ${this.analysisResults.amountSum.mean.toFixed(2)}`);
        console.log(`  Median: ${this.analysisResults.amountSum.median.toFixed(2)}`);
        console.log(`  Standard Deviation: ${this.analysisResults.amountSum.stdDev.toFixed(2)}`);
        // Report account similarities
        console.log(`\nAccount Similarity Analysis:`);
        console.log(`  Similar accounts found: ${patterns.accountSimilarities.length}`);
        patterns.accountSimilarities.slice(0, 5).forEach((sim) => {
            console.log(`  Accounts ${sim.account1} and ${sim.account2}: ${sim.similarity.toFixed(2)}% similar`);
        });
        // Report potential privacy concerns
        console.log(`\nPotential Privacy Risks:`);
        console.log(`  - Account similarity patterns may reveal personal habits`);
        console.log(`  - Distribution patterns can be used to identify account owners`);
        console.log(`  - Transaction frequency may indicate spending behaviors`);
    }
}
exports.PrivacyAttack = PrivacyAttack;
