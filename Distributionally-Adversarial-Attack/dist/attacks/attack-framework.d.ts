import { Transaction, Account } from '../models/transaction';
export declare abstract class AttackFramework {
    protected attackName: string;
    protected targetData: Transaction[] | Account[];
    protected isRunning: boolean;
    constructor(attackName: string);
    /**
     * Set the target data for the attack
     */
    setTargetData(data: Transaction[] | Account[]): void;
    /**
     * Start the attack
     */
    start(): Promise<void>;
    /**
     * Execute the attack logic (to be implemented by subclasses)
     */
    protected abstract execute(): Promise<void>;
    /**
     * Stop the attack
     */
    stop(): void;
    /**
     * Get attack status
     */
    getStatus(): boolean;
    /**
     * Get attack name
     */
    getName(): string;
}
