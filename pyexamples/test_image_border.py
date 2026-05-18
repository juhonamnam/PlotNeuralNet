
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_image( "../examples/fcn8s/cats.jpg", name="test_img_no_border", width=40, height=40, offset="(0,0,0)" ),
    to_image( "../examples/fcn8s/cats.jpg", name="test_img_with_border", width=40, height=40, offset="(0,-10,0)", border="black, thick" ),
    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    with open(namefile+'.tex', 'w') as f:
        for i in arch:
            f.write(i)

if __name__ == '__main__':
    main()
