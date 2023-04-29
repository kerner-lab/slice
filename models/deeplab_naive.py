"""
DeepLabV3+ model with a ResNet-101 backbone for Field Boundary Detection & Instance Segmentation.

Input: 224x224x3
Output: 224x224x3
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import lightning.pytorch as pl
from lightning.pytorch.utilities.model_summary import ModelSummary


class DeepLabV3Plus(pl.LightningModule):
    def __init__(self, num_classes=3, pretrained=True):
        super().__init__()
        self.num_classes = num_classes
        self.pretrained = pretrained
        self.model = models.segmentation.deeplabv3_resnet101(pretrained=self.pretrained, progress=True)
        self.model.classifier[-1] = nn.Conv2d(256, self.num_classes, kernel_size=(1, 1), stride=(1, 1))
        self.model.aux_classifier[-1] = nn.Conv2d(256, self.num_classes, kernel_size=(1, 1), stride=(1, 1))

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = F.cross_entropy(y_hat['out'], y)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.forward(x)
        loss = F.cross_entropy(y_hat['out'], y)
        self.log('val_loss', loss)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

    def summary(self, max_depth=-1):
        return ModelSummary(self, max_depth=max_depth, )


if __name__ == '__main__':
    model = DeepLabV3Plus()
    sample_data = torch.rand(1, 3, 224, 224)
    print(model.summary(1))
    