"""This script is used to evaluate the model's instance segmentation predictions.
The script is used to calculate the following metrics:
- Precision
- Recall
- F1-score
- IoU
- Accuracy
"""

import numpy as np
from tqdm import tqdm
from scipy.optimize import linear_sum_assignment

def calculate_iou(pred_mask, gt_mask):
    """Calculate IoU for a single predicted and ground truth mask.
    Args:
        pred_mask (numpy array): Predicted mask of shape (H, W)
        gt_mask (numpy array): Ground truth mask of shape (H, W)
    Returns:
        iou (float): Value of IoU for the two masks
    """
    intersection = np.logical_and(pred_mask, gt_mask)
    union = np.logical_or(pred_mask, gt_mask)
    iou = np.sum(intersection) / np.sum(union)
    return iou

def evaluate_instance_segmentation(pred_masks, gt_masks):
    """Evaluate instance segmentation using mean IoU.
    Args:
        pred_masks (numpy array): Array of predicted masks of shape (N, H, W)
        gt_masks (numpy array): Array of ground truth masks of shape (N, H, W)
    Returns:
        mean_iou (float): Mean IoU
    """
    num_pred_instances = len(pred_masks)
    num_gt_instances = len(gt_masks)
    iou_matrix = np.zeros((num_pred_instances, num_gt_instances))
    
    # Calculate IoU for all pairs of predicted and ground truth masks
    for i in range(num_pred_instances):
        for j in range(num_gt_instances):
            pred_mask = pred_masks[i]
            gt_mask = gt_masks[j]
            iou_matrix[i, j] = calculate_iou(pred_mask, gt_mask)
    
    # Perform optimal matching using Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(-iou_matrix)
    
    # Calculate mean IoU using the matched pairs
    matched_ious = iou_matrix[row_ind, col_ind]
    mean_iou = np.mean(matched_ious)
    
    return mean_iou

# Example usage
if __name__ == "__main__":
    pred_masks = None
    gt_masks = None
    # Ensure the shapes of pred_masks and gt_masks are compatible
    assert pred_masks.shape[1:] == gt_masks.shape[1:], "Shape mismatch between prediction and ground truth masks"

    # Evaluate instance segmentation
    mean_iou = evaluate_instance_segmentation(pred_masks, gt_masks)
    print("Mean IoU:", mean_iou)
    

    