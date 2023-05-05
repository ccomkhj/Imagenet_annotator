## Rapid Imagenet-style Annotation Generator (Classification)

1. prepare config file
`config/class.yaml`
```yaml
healthy: 0
unhealthy: 1
no plant: 2
```

2. run
`python createClsAnns.py -i {image directory}`

3. type relevant class number

4. if you made mistake, type 'x'. It is logged that you made mistake in which image file.

5. if you want to quit, type 'q'.

### Output
`result/ann_{epoch time}.txt`
`result/log_{epoch time}.txt`
