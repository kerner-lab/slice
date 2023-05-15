import sys
import argparse
from typing import Any, Dict, List

sys.path.append("models/segment-anything")
from utils.dataset import ParcelDataset
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

# Create the parser
parser = argparse.ArgumentParser()
parser.add_argument("--model-type", type=str, default="default", required=True, help="The type of model to load, in ['default', 'vit_h', 'vit_l', 'vit_b']", )
parser.add_argument("--checkpoint", type=str, default="weights/sam_vit_h.pth", required=True, help="The path to the SAM checkpoint to use for mask generation.", )
parser.add_argument("--device", type=str, default="cuda", help="The device to run generation on.")

def parse_masks(masks: List[Dict[str, Any]], path: str) -> Dict:
    """Parse the masks into a dictionary.
    Args:
        masks: The masks to parse.
        path: The path to the image that the masks were generated for.
    Returns:
        A dictionary containing the parsed masks.
    """
    export_masks = []
    for i, mask_data in enumerate(masks[1:]):
        mask = mask_data["segmentation"]
        mask_metadata = {
            "id": str(i),
            "area": str(mask_data["area"]),
            "bbox_x0": str(mask_data["bbox"][0]),
            "bbox_y0": str(mask_data["bbox"][1]),
            "bbox_w": str(mask_data["bbox"][2]),
            "bbox_h": str(mask_data["bbox"][3]),
            "point_input_x": str(mask_data["point_coords"][0][0]),
            "point_input_y": str(mask_data["point_coords"][0][1]),
            "predicted_iou": str(mask_data["predicted_iou"]),
            "stability_score": str(mask_data["stability_score"]),
            "crop_box_x0": str(mask_data["crop_box"][0]),
            "crop_box_y0": str(mask_data["crop_box"][1]),
            "crop_box_w": str(mask_data["crop_box"][2]),
            "crop_box_h": str(mask_data["crop_box"][3]),
            "image": mask,
        }
        export_masks.append(mask_metadata)

    return export_masks


def main(args: argparse.Namespace) -> None:
    """Run the main function."""
    # Load SAM and setup configs
    sam = sam_model_registry[args.model_type](checkpoint=args.checkpoint)
    _ = sam.to(device=args.device)
    output_mode = "binary_mask"
    generator = SamAutomaticMaskGenerator(sam, output_mode=output_mode, **amg_kwargs)

    # Load the dataset and get a random image
    dataset = ParcelDataset(path="data/france/dataset_chunk/")
    image, label = dataset[0]

    # Generate the mask
    masks = generator.generate(image)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
    
    
