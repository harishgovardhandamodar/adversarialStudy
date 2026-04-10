"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AttackFramework = void 0;
class AttackFramework {
    constructor(attackName) {
        this.attackName = attackName;
        this.targetData = [];
        this.isRunning = false;
    }
    /**
     * Set the target data for the attack
     */
    setTargetData(data) {
        this.targetData = data;
    }
    /**
     * Start the attack
     */
    async start() {
        this.isRunning = true;
        console.log(`Starting ${this.attackName} attack...`);
        // Validation
        if (!this.targetData || this.targetData.length === 0) {
            throw new Error('No target data provided for attack');
        }
        try {
            await this.execute();
        }
        catch (error) {
            console.error(`Attack ${this.attackName} failed:`, error);
            throw error;
        }
        finally {
            this.isRunning = false;
            console.log(`Attack ${this.attackName} completed.`);
        }
    }
    /**
     * Stop the attack
     */
    stop() {
        this.isRunning = false;
        console.log(`Attack ${this.attackName} stopped.`);
    }
    /**
     * Get attack status
     */
    getStatus() {
        return this.isRunning;
    }
    /**
     * Get attack name
     */
    getName() {
        return this.attackName;
    }
}
exports.AttackFramework = AttackFramework;
