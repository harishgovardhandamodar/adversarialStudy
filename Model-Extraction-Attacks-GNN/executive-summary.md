# Executive Summary: Model Extraction Attacks on GNNs for Bank Fraud Detection

## Project Overview

This project implements a comprehensive framework for studying Model Extraction Attacks (MEAs) against Graph Neural Networks (GNNs) used in financial fraud detection. The system simulates adversaries with varying levels of knowledge about target GNNs to demonstrate how attackers can build surrogate models with significant fidelity to the original, potentially compromising system security and privacy.

## Key Findings

### Attack Effectiveness
- **High Knowledge Attacks** (Types 4, 5, 6): Achieve fidelity above 0.8
- **Medium Knowledge Attacks** (Types 2, 3): Achieve fidelity between 0.6-0.75  
- **Low Knowledge Attacks** (Types 0, 1): Achieve fidelity typically below 0.6

### Critical Vulnerabilities
1. **Structure Knowledge**: Adversaries with graph topology information significantly improve attack success
2. **Attribute Information**: Even partial attribute knowledge enables effective attacks
3. **Shadow Dataset Access**: Access to auxiliary training data provides crucial learning opportunities

## Business Impact

### Risks
- **Intellectual Property Theft**: Attackers can extract model weights and structure
- **System Compromise**: Surrogate models can be used to predict and exploit system vulnerabilities  
- **Reputational Damage**: Successful attacks can undermine trust in financial systems
- **Regulatory Compliance**: Potential violations of data protection regulations

### Security Implications
- GNN fraud detection systems are vulnerable to sophisticated adversarial attacks
- Even simple GNN models can be extracted with reasonable accuracy
- Attack effectiveness is heavily dependent on adversary knowledge level

## Recommendations

### For Data Scientists
- Implement adversarial robustness in GNN model design
- Consider differential privacy techniques for model protection
- Regular security testing of machine learning systems
- Develop defensive mechanisms for model APIs

### For Compliance Officers  
- Establish strict access controls for model inference APIs
- Implement audit logging for model usage
- Address vulnerabilities proactively through security testing
- Ensure compliance with data protection regulations

### For Executives
- Allocate resources for adversarial robustness in AI/ML systems
- Develop protocols for model protection and security monitoring
- Understand business risks from potential model extraction attacks
- Prioritize investment in AI/ML security solutions

## Conclusion

This framework demonstrates that GNN-based fraud detection models are vulnerable to model extraction attacks, especially when attackers have partial knowledge of graph structure and attributes. Organizations must take proactive steps to protect their machine learning models and implement robust security measures to defend against these emerging threats.