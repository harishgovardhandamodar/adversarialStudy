# Diffusion Model for Differential Privacy Denoising

## Goal
Demonstrate that diffusion models can recover useful information from differentially private (noise-corrupted) tabular data.

## Method
1. Generate synthetic credit card transaction data
2. Add Laplace noise (ε = 1.0) for differential privacy
3. Train a diffusion model to learn the reverse noising process
4. Visualize distribution comparison and denoising steps

## Key Results
- Diffusion model successfully denoised private data (visualized across multiple timesteps)
- Original and private datasets maintain similar marginal distributions
- Recovered data retains statistical structure while privacy is theoretically guaranteed

## Visual Outputs
- `Data-Distribution-Comparison.png` — original vs private distribution
- `differential_privacy_results.png` — noise addition visualization
- `diffusion_denoising_results_originalvsnoisy.png` — denoising progression

## Takeaway
Diffusion models offer a promising bridge between differential privacy and data utility. However, this also means DP guarantees can be weakened if adversaries have access to powerful generative models.

## Files
- `diffusion-model/Denoising-Diffusion-Model-DP-Data/final_diffusion_dp_demo.ipynb`
- `diffusion-model/Denoising-Diffusion-Model-DP-Data/*.png`
