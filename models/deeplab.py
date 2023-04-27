import torch
import torchvision
import torch.nn as nn
import lightning.pytorch as pl

model = torchvision.models.segmentation.deeplabv3_resnet50(pretrained=True)
model.classifier[-1] = nn.Conv2d(256, 2, kernel_size=(1, 1), stride=(1, 1))
model.aux_classifier[-1] = nn.Conv2d(256, 2, kernel_size=(1, 1), stride=(1, 1))

class DeepLab(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = model

    def forward(self, x):
        return self.model(x)['out']

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = nn.functional.cross_entropy(y_hat, y)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = nn.functional.cross_entropy(y_hat, y)
        self.log('val_loss', loss)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)