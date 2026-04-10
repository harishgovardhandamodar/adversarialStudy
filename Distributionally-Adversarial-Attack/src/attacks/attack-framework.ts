// Base attack framework for adversarial attacks on transaction data
import { Transaction, Account } from '../models/transaction';

export abstract class AttackFramework {
  protected attackName: string;
  protected targetData: Transaction[] | Account[];
  protected isRunning: boolean;

  constructor(attackName: string) {
    this.attackName = attackName;
    this.targetData = [];
    this.isRunning = false;
  }

  /**
   * Set the target data for the attack
   */
  setTargetData(data: Transaction[] | Account[]) {
    this.targetData = data;
  }

  /**
   * Start the attack
   */
  async start(): Promise<void> {
    this.isRunning = true;
    console.log(`Starting ${this.attackName} attack...`);
    
    // Validation
    if (!this.targetData || this.targetData.length === 0) {
      throw new Error('No target data provided for attack');
    }

    try {
      await this.execute();
    } catch (error) {
      console.error(`Attack ${this.attackName} failed:`, error);
      throw error;
    } finally {
      this.isRunning = false;
      console.log(`Attack ${this.attackName} completed.`);
    }
  }

  /**
   * Execute the attack logic (to be implemented by subclasses)
   */
  protected abstract execute(): Promise<void>;

  /**
   * Stop the attack
   */
  stop(): void {
    this.isRunning = false;
    console.log(`Attack ${this.attackName} stopped.`);
  }

  /**
   * Get attack status
   */
  getStatus(): boolean {
    return this.isRunning;
  }

  /**
   * Get attack name
   */
  getName(): string {
    return this.attackName;
  }
}