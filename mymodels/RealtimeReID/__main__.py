import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

def to_merge_connection( ofs: list[str], to: str, path="|-"):
    tex_str = ""
    for idx, of in enumerate(ofs):
        ts =  """
\draw [connection]  ("""+of+""") -- node {\midarrow} ("""+of+path+to+""")"""
        if idx == 0:
            ts += " -- node {\midarrow} ("+to+");\n"
        else:
            ts += ";\n"

        tex_str += ts

    return tex_str

arch = [ 
    to_head('../..'), 
    to_cor(),
    to_begin(),
    
    to_image(pathfile='./input.jpg', width=20, height=60, name="input",
             caption="Input Image"),

    to_ConvConvRelu( name='bb1', offset="(4,0,0)", to="(input-east)", width=(2,2), height=48, depth=16, show_labels=False ),
    
    to_connection( "input", "bb1" ),

    to_Pool(name="bb1-fm", offset="(2,0,0)", to="(bb1-east)", width=1, height=48, depth=16, opacity=0.5),

    to_ConvConvRelu( name='bb2', offset="(2,0,0)", to="(bb1-fm-east)", width=(4,4), height=36, depth=12, show_labels=False ),

    to_connection( "bb1", "bb2"),

    to_Pool(name="bb2-fm", offset="(2,0,0)", to="(bb2-east)", width=2, height=36, depth=12, opacity=0.5),

    to_ConvConvRelu( name='bb3', offset="(2,0,0)", to="(bb2-fm-east)", width=(8,8), height=24, depth=8, show_labels=False ),

    to_connection( "bb2", "bb3"),

    to_Pool(name="bb3-fm", offset="(2,0,0)", to="(bb3-east)", width=4, height=24, depth=8, opacity=0.5),

    to_ConvConvRelu( name='bb4', offset="(2,0,0)", to="(bb3-fm-east)", width=(16,16), height=12, depth=4, show_labels=False ),

    to_connection( "bb3", "bb4"),

    to_Pool(name="bb4-fm", offset="(2,0,0)", to="(bb4-east)", width=8, height=12, depth=4, opacity=0.5),

    to_connection( "bb4", "bb4-fm"),

    to_ConvConvRelu(name='feature-conv', offset="(2,8,0)",
                    to="(bb4-fm-east)", width=(4,4), height=24,
                    depth=8, show_labels=False),

    to_ConvConvRelu(name='segment-conv', offset="(2,-8,0)",
                    to="(bb4-fm-east)", width=(4,4), height=24,
                    depth=8, show_labels=False),

    to_merge_connection(["bb1-fm-north", "bb2-fm-north"],
                        "feature-conv-west", path="|-"),
    to_merge_connection(["bb1-fm-south", "bb2-fm-south",
                         "bb3-fm-south", "bb4-fm-south"],
                        "segment-conv-west", path="|-"),

    to_Pool(name="feature", offset="(2,0,0)",
            to="(feature-conv-east)", width=4, height=24,
            depth=8, opacity=0.5,
            caption="Embedding Feature Map"),
    
    to_image(pathfile="./input.jpg", name="segment", offset="(2,0,0)",
             to="(segment-conv-east)", width=8, height=24,
             # opacity=0.5,
             caption="Body Part Segmentation"),

    to_connection("feature-conv", "feature"),
    to_connection("segment-conv", "segment"),

    to_image(pathfile="./input.jpg", name="sg1", offset="(16,16,0)",
             to="(bb4-fm-east)", width=8, height=24,
             caption="Head"),
    to_image(pathfile="./input.jpg", name="sg2", offset="(16,8,0)",
             to="(bb4-fm-east)", width=8, height=24,
             caption="Torso"),
    to_image(pathfile="./input.jpg", name="sg3", offset="(16,0,0)",
             to="(bb4-fm-east)", width=8, height=24,
             caption="Arms"),
    to_image(pathfile="./input.jpg", name="sg4", offset="(16,-8,0)",
             to="(bb4-fm-east)", width=8, height=24,
             caption="Upper Legs"),
    to_image(pathfile="./input.jpg", name="sg5", offset="(16,-16,0)",
             to="(bb4-fm-east)", width=8, height=24,
             caption="Lower Legs"),

    to_connection("segment", "sg1"),
    to_connection("segment", "sg2"),
    to_connection("segment", "sg3"),
    to_connection("segment", "sg4"),
    to_connection("segment", "sg5"),

    to_connection("feature", "sg1"),
    to_connection("feature", "sg2"),
    to_connection("feature", "sg3"),
    to_connection("feature", "sg4"),
    to_connection("feature", "sg5"),

    to_UnPool(name="emb1", offset="(2,0,0)",
              to="(sg1-east)", width=8, height=1,
              depth=1, opacity=0.5),
    to_UnPool(name="emb2", offset="(2,0,0)",
              to="(sg2-east)", width=8, height=1,
              depth=1, opacity=0.5),
    to_UnPool(name="emb3", offset="(2,0,0)",
              to="(sg3-east)", width=8, height=1,
              depth=1, opacity=0.5),
    to_UnPool(name="emb4", offset="(2,0,0)",
              to="(sg4-east)", width=8, height=1,
              depth=1, opacity=0.5),
    to_UnPool(name="emb5", offset="(2,0,0)",
              to="(sg5-east)", width=8, height=1,
              depth=1, opacity=0.5),

    to_connection("sg1", "emb1"),
    to_connection("sg2", "emb2"),
    to_connection("sg3", "emb3"),
    to_connection("sg4", "emb4"),
    to_connection("sg5", "emb5"),

    to_end() 
    ]


def main():
    namefile = os.path.dirname(sys.argv[0])
    namefile = os.path.join(namefile, "main.tex")
    to_generate(arch, namefile)

if __name__ == '__main__':
    main()
    
