import { AttackFramework } from './attack-framework';
export declare class PrivacyAttack extends AttackFramework {
    private analysisResults;
    constructor();
    /**
     * Execute privacy attack using distributional analysis
     */
    protected execute(): Promise<void>;
    /**
     * Perform distributional analysis on transaction data
     */
    private performDistributionalAnalysis;
    /**
     * Extract patterns from distributional analysis
     */
    private extractPatterns;
    /**
     * Calculate account similarity based on transaction behavior
     */
    private calculateAccountSimilarity;
    /**
     * Calculate mean value
     */
    private calculateMean;
    /**
     * Calculate median value
     */
    private calculateMedian;
    /**
     * Calculate standard deviation
     */
    private calculateStandardDeviation;
    /**
     * Report findings without exposing raw sensitive data
     */
    private reportFindings;
}
