# SVD Low-Rank Approximation Engine
# Purpose: Digital Signal Processing via Singular Value Decomposition

import numpy as np
from PIL import Image, ImageFilter

def apply_low_pass_filter(image_array, radius):
    """
    Applies a Gaussian Blur to kill high-frequency noise (like the gate 
    from Evangelion's Terminal Dogma).
    """
    img = Image.fromarray(image_array)
    img_blurred = img.filter(ImageFilter.GaussianBlur(radius=radius))
    return np.array(img_blurred, dtype=np.float64)


def compute_svd_compression(image_array, k_target):
    """
    Performs SVD and truncates the matrices to rank k.
    "I'm using Singular Values as the mother of all omelettes, Jack!"
    """
    # U: Left singular vectors, S: Singular values, Vt: Right singular vectors
    U, S, Vt = np.linalg.svd(image_array, full_matrices=False)
    
    # Calculate target rank k based on percentage
    k = int(len(S) * k_target)
    k = max(k, 1) # Ensure at least rank 1 (don't let the soul be empty like GLT)
    
    # Reconstruct the approximation: A_k = U_k * Sigma_k * V_k^T
    # This is the 'Low-Rank' magic from Boyd's VMLS
    A_k = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
    
    return A_k, k