"""
(C) Copyright 2021 IBM Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Created on June 30, 2021

"""
from typing import Optional
from fuse.data.datasets.dataset_wrap_seq_to_dict import DatasetWrapSeqToDict
from torchvision import transforms

import torchvision

from fuse.data import DatasetDefault

class MNIST:
    """
    FuseMedML style of MNIST dataset: http://yann.lecun.com/exdb/mnist/ 
    """
    # bump whenever the static pipeline modified
    MNIST_DATASET_VER = 0

    @staticmethod
    def dataset(cache_dir: Optional[str] = None, train: bool = True) -> DatasetDefault:
        """
        Get mnist dataset - each sample includes: 'data.image', 'data.label' and 'data.sample_id'
        :param cache_dir: optional - destination to cache mnist
        :param train: If True, creates dataset from ``train-images-idx3-ubyte``,
            otherwise from ``t10k-images-idx3-ubyte``.
        """        
        
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        # Create dataset
        torch_train_dataset = torchvision.datasets.MNIST(cache_dir, download=cache_dir is not None, train=train, transform=transform)
        # wrapping torch dataset
        train_dataset = DatasetWrapSeqToDict(name=f'mnist-{train}', dataset=torch_train_dataset, sample_keys=('data.image', 'data.label'))
        train_dataset.create()
        return train_dataset