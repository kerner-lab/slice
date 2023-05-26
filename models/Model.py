import numpy as np
import matplotlib.pyplot as plt
import gc
from PIL import Image, ImageOps
import torch
from transformers import SamModel, SamProcessor, SamImageProcessor
from collections import defaultdict

class SAM_Network:
    def __init__(self, model_type):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SamModel.from_pretrained("facebook/sam-vit-"+model_type).to(self.device)
        self.processor = SamProcessor.from_pretrained("facebook/sam-vit-"+model_type)
        self.image_processor = SamImageProcessor()
    
    
    def _overlay_ind_mask(self, mask, ax, random_color=False):
        if random_color:
            color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
        else:
            color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        ax.imshow(mask_image)
        del mask
        gc.collect()

    def overlay_mask(self, raw_image, masks):
        plt.imshow(np.array(raw_image))
        ax = plt.gca()
        ax.set_autoscale_on(False)
        for mask in masks:
            self._overlay_ind_mask(mask, ax=ax, random_color=True)
        plt.axis("off")
        plt.show()
        del mask
        gc.collect()
    
    def load_image(self, image_path):
        image = Image.open(image_path)
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        return image
    
    def preprocess(
        self,
        image,
        points_per_batch=64,
        crops_n_layers: int = 0,
        crop_overlap_ratio: float = 512 / 1500,
        points_per_crop: int = 32,
        crop_n_points_downscale_factor: int = 1,
    ):
        target_size = self.image_processor.size["longest_edge"]
        crop_boxes, grid_points, cropped_images, input_labels = self.image_processor.generate_crop_boxes(
            image, target_size, crops_n_layers, crop_overlap_ratio, points_per_crop, crop_n_points_downscale_factor, device=self.device
        )
        model_inputs = self.processor(images=cropped_images, return_tensors="pt").to(self.device)
        with torch.no_grad():
            image_embeddings = self.model.vision_encoder(model_inputs.pop("pixel_values"))[0]
            model_inputs["image_embeddings"] = image_embeddings

        n_points = grid_points.shape[1]
        points_per_batch = points_per_batch if points_per_batch is not None else n_points

        if points_per_batch <= 0:
            raise ValueError(
                "Cannot have points_per_batch<=0. Must be >=1 to returned batched outputs. "
                "To return all points at once, set points_per_batch to None"
            )

        for i in range(0, n_points, points_per_batch):
            batched_points = grid_points[:, i : i + points_per_batch, :, :]
            labels = input_labels[:, i : i + points_per_batch]
            is_last = i == n_points - points_per_batch
            yield {
                "input_points": batched_points,
                "input_labels": labels,
                "input_boxes": crop_boxes,
                "is_last": is_last,
                **model_inputs,
            }
    
    
    def forward(
        self,
        model_inputs,
        pred_iou_thresh=0.88,
        stability_score_thresh=0.95,
        mask_threshold=0,
        stability_score_offset=1,
    ):
        input_boxes = model_inputs.pop("input_boxes")
        is_last = model_inputs.pop("is_last")
        original_sizes = model_inputs.pop("original_sizes").tolist()
        reshaped_input_sizes = model_inputs.pop("reshaped_input_sizes").tolist()
        
        model_outputs = self.model(**model_inputs)

        # post processing happens here in order to avoid CPU GPU copies of ALL the masks
        low_resolution_masks = model_outputs["pred_masks"]
        masks = self.image_processor.post_process_masks(
            low_resolution_masks, original_sizes, reshaped_input_sizes, mask_threshold, binarize=False
        )
        iou_scores = model_outputs["iou_scores"]
        masks, iou_scores, boxes = self.image_processor.filter_masks(
            masks[0],
            iou_scores[0],
            original_sizes[0],
            input_boxes[0],
            pred_iou_thresh,
            stability_score_thresh,
            mask_threshold,
            stability_score_offset,
        )
        return {
            "masks": masks,
            "is_last": is_last,
            "boxes": boxes,
            "iou_scores": iou_scores,
        }
    
    def postprocess(
        self,
        model_outputs,
        output_rle_mask=False,
        output_bboxes_mask=False,
        crops_nms_thresh=0.7,
    ):
        all_scores = []
        all_masks = []
        all_boxes = []
        for model_output in model_outputs:
            all_scores.append(model_output.pop("iou_scores"))
            all_masks.extend(model_output.pop("masks"))
            all_boxes.append(model_output.pop("boxes"))

        all_scores = torch.cat(all_scores)
        all_boxes = torch.cat(all_boxes)
        output_masks, iou_scores, rle_mask, bounding_boxes = self.image_processor.post_process_for_mask_generation(
            all_masks, all_scores, all_boxes, crops_nms_thresh
        )

        extra = defaultdict(list)
        for output in model_outputs:
            for k, v in output.items():
                extra[k].append(v)

        optional = {}
        if output_rle_mask:
            optional["rle_mask"] = rle_mask

        if output_bboxes_mask:
            optional["bounding_boxes"] = bounding_boxes

        return {"masks": output_masks, "scores": iou_scores}
    
    def infer_single(self, inputs, points_per_batch = 128):
        with torch.no_grad():
            all_outputs = []
            for model_inputs in self.preprocess(inputs):
                model_outputs = self.forward(model_inputs)
                all_outputs.append(model_outputs)
            outputs = self.postprocess(all_outputs)
        return outputs