## Rapid Imagenet-style Annotation Generator (Classification)

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
healthy: 0
unhealthy: 1
no plant: 2
```

2. run

if you want to create annotation only

`python createClsAnns.py -i {image directory}`

if you want to copy images, too

`python createClsAnns.py -s -i {image directory}`

3. type relevant class number per image

4. if you made mistake, type 'x'. It is logged that you made mistake in which image file.

5. if you want to quit, type 'q'.

### Output
`result/ann_{epoch time}.txt`

`result/log_{epoch time}.txt`
