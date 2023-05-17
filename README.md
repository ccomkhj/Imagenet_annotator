## Rapid Imagenet-style Annotation Generator (Classification)

This is an effective tool to prepare annotation sample with text annotation.
If you want to filter using folder, check this [repo](https://github.com/ccomkhj/filterObjs).

0. setup
```bash
conda create -n ann python=3.11
conda activate ann
git clone https://github.com/ccomkhj/Imagenet_annotator.git
cd Imagenet_annotator
pip install -r requirements.txt
```

1. prepare config file
`config/class.yaml`
```yaml
noplants: 0
healthy: 1
unhealthy: 2
```

2. run

if you want to create annotation only

`python createClsAnns.py -i {image directory}`

if you want to copy images

`python createClsAnns.py -s -i {image directory}`

if you want to copy images and save them based on the class name

`python createClsAnns.py -s -f -i {image directory}`

if you want to start from specific index, (it is useful if you begin with the previous work.)

`python createClsAnns.py -s -b {index to begin with} -i {image directory}`

3. type relevant class number per image

4. if you made mistake, type 'x'. It is logged that you made mistake in which image file.

5. if you want to quit, type 'q'.

### Output
`result/ann_{epoch time}.txt`

`result/log_{epoch time}.txt`


## Wanna split train and validation set?

`python split.py -i {image directory} -a {annotation text file} -r 0.8`