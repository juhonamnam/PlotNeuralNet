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

model_arch = [ 
    to_head('../..'), 
    to_cor(),
    to_begin(),
    
    to_image(pathfile='./input.jpg', width=20, height=60, name="input",
             caption="Input Image"),

    to_ConvConvRelu(name='bb1', offset="(4,0,0)", to="(input-east)",
                    width=(2,2), height=48, depth=16, show_labels=False,
                    caption="Conv"),
    
    to_connection( "input-east", "bb1-west" ),

    to_Pool(name="bb1-fm", offset="(2,0,0)", to="(bb1-east)",
            width=1, height=48, depth=16, opacity=0.5,
            caption="Feature Map 1"),

    to_ConvConvRelu(name='bb2', offset="(2,0,0)", to="(bb1-fm-east)",
                    width=(4,4), height=36, depth=12, show_labels=False,
                    caption="Conv"),

    to_connection( "bb1-east", "bb2-west"),

    to_Pool(name="bb2-fm", offset="(2,0,0)", to="(bb2-east)",
            width=2, height=36, depth=12, opacity=0.5,
            caption="Feature Map 2"),

    to_ConvConvRelu(name='bb3', offset="(2,0,0)", to="(bb2-fm-east)",
                    width=(8,8), height=24, depth=8, show_labels=False,
                    caption="Conv"),

    to_connection( "bb2-east", "bb3-west"),

    to_Pool(name="bb3-fm", offset="(2,0,0)", to="(bb3-east)",
            width=4, height=24, depth=8, opacity=0.5,
            caption="Feature Map 3"),

    to_ConvConvRelu(name='bb4', offset="(2,0,0)", to="(bb3-fm-east)",
                    width=(16,16), height=12, depth=4, show_labels=False,
                    caption="Conv"),

    to_connection( "bb3-east", "bb4-west"),

    to_Pool(name="bb4-fm", offset="(2,0,0)", to="(bb4-east)",
            width=8, height=12, depth=4, opacity=0.5,
            caption="Feature Map 4"),

    to_connection( "bb4-east", "bb4-fm-west"),

    to_ConvConvRelu(name='feature-conv', offset="(2,-8,0)",
                    to="(bb4-fm-east)", width=(6,6), height=24,
                    depth=8, show_labels=False,
                    caption="FPN + Conv"),

    to_ConvConvRelu(name='segment-conv', offset="(2,8,0)",
                    to="(bb4-fm-east)", width=(6,6), height=24,
                    depth=8, show_labels=False,
                    caption="FPN + Conv"),

    to_merge_connection(["bb1-fm-south", "bb2-fm-south"],
                        "feature-conv-west", path="|-"),
    to_merge_connection(["bb1-fm-north", "bb2-fm-north",
                         "bb3-fm-north", "bb4-fm-north"],
                        "segment-conv-west", path="|-"),

    to_Pool(name="feature", offset="(2,0,0)",
            to="(feature-conv-east)", width=4, height=24,
            depth=8, opacity=0.5,
            caption="Embedding Feature Map"),
    
    to_image(pathfile="./lowerlegs.png", name="sgt1", offset="(3,0.4,-1)",
             to="(segment-conv-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./upperlegs.png", name="sgt2", offset="(3,0.2,-0.5)",
             to="(segment-conv-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./arms.png", name="sgt3", offset="(3,0,0)",
             to="(segment-conv-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./torso.png", name="sgt4", offset="(3,-0.2,0.5)",
             to="(segment-conv-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./head.png", name="sgt5", offset="(3,-0.4,1)",
             to="(segment-conv-east)", width=8, height=24, border="black, thick",
             caption="Body Part Segmentation"),

    to_connection("feature-conv-east", "feature-west"),
    to_connection("segment-conv-east", "sgt3-west"),

    to_image(pathfile="./head.png", name="sg1", offset="(16,16,0)",
             to="(bb4-fm-east)", width=8, height=24, border="black, thick",
             caption="Head"),
    to_image(pathfile="./torso.png", name="sg2", offset="(16,8,0)",
             to="(bb4-fm-east)", width=8, height=24, border="black, thick",
             caption="Torso"),
    to_image(pathfile="./arms.png", name="sg3", offset="(16,0,0)",
             to="(bb4-fm-east)", width=8, height=24, border="black, thick",
             caption="Arms"),
    to_image(pathfile="./upperlegs.png", name="sg4", offset="(16,-8,0)",
             to="(bb4-fm-east)", width=8, height=24, border="black, thick",
             caption="Upper Legs"),
    to_image(pathfile="./lowerlegs.png", name="sg5", offset="(16,-16,0)",
             to="(bb4-fm-east)", width=8, height=24, border="black, thick",
             caption="Lower Legs"),

    to_connection("sgt1-east", "sg1-west"),
    to_connection("sgt1-east", "sg2-west"),
    to_connection("sgt1-east", "sg3-west"),
    to_connection("sgt1-east", "sg4-west"),
    to_connection("sgt1-east", "sg5-west"),

    to_connection("feature-east", "sg1-west"),
    to_connection("feature-east", "sg2-west"),
    to_connection("feature-east", "sg3-west"),
    to_connection("feature-east", "sg4-west"),
    to_connection("feature-east", "sg5-west"),

    to_UnPool(name="emb1", offset="(2,0,0)",
              to="(sg1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Embedding 1"),
    to_UnPool(name="emb2", offset="(2,0,0)",
              to="(sg2-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Embedding 2"),
    to_UnPool(name="emb3", offset="(2,0,0)",
              to="(sg3-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Embedding 3"),
    to_UnPool(name="emb4", offset="(2,0,0)",
              to="(sg4-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Embedding 4"),
    to_UnPool(name="emb5", offset="(2,0,0)",
              to="(sg5-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Embedding 5"),

    to_connection("sg1-east", "emb1-west"),
    to_connection("sg2-east", "emb2-west"),
    to_connection("sg3-east", "emb3-west"),
    to_connection("sg4-east", "emb4-west"),
    to_connection("sg5-east", "emb5-west"),

    to_end() 
]

comp_arch = [
    to_head('../..'), 
    to_cor(),
    to_begin(),
    
    to_image(pathfile='./input.jpg', width=20, height=60, name="input1"),

    to_Conv(name='model1', offset="(3,0,0)", to="(input1-east)",
            width=24, height=16, depth=16, show_labels=False,
            caption='ReID Model'),

    to_connection("input1-east", "model1-west"),

    to_UnPool(name="emb11", offset="(5,6,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Head"),
    to_UnPool(name="emb12", offset="(5,3,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Torso"),
    to_UnPool(name="emb13", offset="(5,0,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Arms"),
    to_UnPool(name="emb14", offset="(5,-3,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Upper Legs"),
    to_UnPool(name="emb15", offset="(5,-6,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Lower Legs"),

    to_connection("model1-east", "emb11-west"),
    to_connection("model1-east", "emb12-west"),
    to_connection("model1-east", "emb13-west"),
    to_connection("model1-east", "emb14-west"),
    to_connection("model1-east", "emb15-west"),

    to_UnPool(name="emb21", offset="(10,0,0)",
              to="(emb11-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Head"),
    to_UnPool(name="emb22", offset="(10,0,0)",
              to="(emb12-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Torso"),
    to_UnPool(name="emb23", offset="(10,0,0)",
              to="(emb13-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Arms"),
    to_UnPool(name="emb24", offset="(10,0,0)",
              to="(emb14-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Upper Legs"),
    to_UnPool(name="emb25", offset="(10,0,0)",
              to="(emb15-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Lower Legs"),

    to_connection_double("emb11-east", "emb21-west"),
    to_connection_double("emb12-east", "emb22-west"),
    to_connection_double("emb13-east", "emb23-west"),
    to_connection_double("emb14-east", "emb24-west"),
    to_connection_double("emb15-east", "emb25-west"),

    to_Conv(name='model2', offset="(5,0,0)", to="(emb23-east)",
            width=24, height=16, depth=16, show_labels=False,
            caption='ReID Model'),

    to_connection("model2-west", "emb21-east"),
    to_connection("model2-west", "emb22-east"),
    to_connection("model2-west", "emb23-east"),
    to_connection("model2-west", "emb24-east"),
    to_connection("model2-west", "emb25-east"),

    to_image(pathfile='./input2.jpg', offset="(5,0,0)",
             to="(model2-east)", width=20, height=60, name="input2"),

    to_connection("input2-west", "model2-east"),

    to_end() 
]


def main():
    dir_path = os.path.dirname(sys.argv[0])

    model_namefile = os.path.join(dir_path, "model.tex")
    to_generate(model_arch, model_namefile)

    comp_namefile = os.path.join(dir_path, "comp.tex")
    to_generate(comp_arch, comp_namefile)

if __name__ == '__main__':
    main()
    
