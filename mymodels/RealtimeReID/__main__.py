import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

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

    to_ConvConvRelu(name='bb2', offset="(2,0,0)", to="(bb1-east)",
                    width=(4,4), height=36, depth=12, show_labels=False,
                    caption="Conv"),

    to_connection( "bb1-east", "bb2-west"),

    to_Pool(name="bb2-fm", offset="(2,0,0)", to="(bb2-east)",
            width=2, height=36, depth=12, opacity=0.5,
            caption="Feature Map 1"),

    to_ConvConvRelu(name='bb3', offset="(2,0,0)", to="(bb2-fm-east)",
                    width=(8,8), height=24, depth=8, show_labels=False,
                    caption="Conv"),

    to_connection( "bb2-east", "bb3-west"),

    to_Pool(name="bb3-fm", offset="(2,0,0)", to="(bb3-east)",
            width=4, height=24, depth=8, opacity=0.5,
            caption="Feature Map 2"),

    to_ConvConvRelu(name='bb4', offset="(2,0,0)", to="(bb3-fm-east)",
                    width=(16,16), height=12, depth=4, show_labels=False,
                    caption="Conv"),

    to_connection( "bb3-east", "bb4-west"),

    to_Pool(name="bb4-fm", offset="(2,0,0)", to="(bb4-east)",
            width=8, height=12, depth=4, opacity=0.5,
            caption="Feature Map 3"),

    to_connection( "bb4-east", "bb4-fm-west"),

    to_Sum(name="fm-merge", offset="(1,0,0)", to="(bb4-fm-east)", radius=2.5,
           opacity=0.6),

    to_skip( of='bb2-fm', to='fm-merge', pos=1.25),    
    to_skip( of='bb3-fm', to='fm-merge', pos=1.25),    

    to_Pool(name="bb4-fm", offset="(2,0,0)", to="(bb4-east)",
            width=8, height=12, depth=4, opacity=0.5),

    to_ConvConvRelu(name='fpn', offset="(2,0,0)",
                    to="(bb4-fm-east)", width=(6,6), height=24,
                    depth=8, show_labels=False,
                    caption="FPN + Conv"),

    to_connection( "bb4-fm-east", "fpn-west", midarrow=False),

    to_Pool(name="feature", offset="(3,-8,0)",
            to="(fpn-east)", width=4, height=24,
            depth=8, opacity=0.5,
            caption="Embedding Feature Map"),
    
    to_image(pathfile="./lowerleg.png", name="sgt1", offset="(3,8.5,-1)",
             to="(fpn-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./upperleg.png", name="sgt2", offset="(3,8.3,-0.5)",
             to="(fpn-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./arm.png", name="sgt3", offset="(3,8.1,0)",
             to="(fpn-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./torso.png", name="sgt4", offset="(3,7.9,0.5)",
             to="(fpn-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./head.png", name="sgt5", offset="(3,7.7,1)",
             to="(fpn-east)", width=8, height=24, border="black, thick"),
    to_image(pathfile="./wholebody.png", name="sgt6", offset="(3,7.5,1)",
             to="(fpn-east)", width=8, height=24, border="black, thick",
             caption="Body Part Attention"),

    to_connection("fpn-east", "feature-west"),
    to_connection("fpn-east", "sgt3-west"),

    to_image(pathfile="./head.png", name="sg1", offset="(16,20,0)",
             to="(fpn-east)", width=8, height=24, border="black, thick",
             caption="Head"),
    to_image(pathfile="./torso.png", name="sg2", offset="(16,12,0)",
             to="(fpn-east)", width=8, height=24, border="black, thick",
             caption="Torso"),
    to_image(pathfile="./arm.png", name="sg3", offset="(16,4,0)",
             to="(fpn-east)", width=8, height=24, border="black, thick",
             caption="Arms"),
    to_image(pathfile="./upperleg.png", name="sg4", offset="(16,-4,0)",
             to="(fpn-east)", width=8, height=24, border="black, thick",
             caption="Upper Legs"),
    to_image(pathfile="./lowerleg.png", name="sg5", offset="(16,-12,0)",
             to="(fpn-east)", width=8, height=24, border="black, thick",
             caption="Lower Legs"),
    to_image(pathfile="./wholebody.png", name="sg6", offset="(16,-20,0)",
             to="(fpn-east)", width=8, height=24, border="black, thick",
             caption="Whole Body"),

    to_connection("sgt1-east", "sg1-west"),
    to_connection("sgt1-east", "sg2-west"),
    to_connection("sgt1-east", "sg3-west"),
    to_connection("sgt1-east", "sg4-west"),
    to_connection("sgt1-east", "sg5-west"),
    to_connection("sgt1-east", "sg6-west"),

    to_connection("feature-east", "sg1-west"),
    to_connection("feature-east", "sg2-west"),
    to_connection("feature-east", "sg3-west"),
    to_connection("feature-east", "sg4-west"),
    to_connection("feature-east", "sg5-west"),
    to_connection("feature-east", "sg6-west"),

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
    to_UnPool(name="emb6", offset="(2,0,0)",
              to="(sg6-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Embedding 6"),

    to_connection("sg1-east", "emb1-west"),
    to_connection("sg2-east", "emb2-west"),
    to_connection("sg3-east", "emb3-west"),
    to_connection("sg4-east", "emb4-west"),
    to_connection("sg5-east", "emb5-west"),
    to_connection("sg6-east", "emb6-west"),

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

    to_UnPool(name="emb11", offset="(5,10,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Head"),
    to_UnPool(name="emb12", offset="(5,6,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Torso"),
    to_UnPool(name="emb13", offset="(5,2,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Arms"),
    to_UnPool(name="emb14", offset="(5,-2,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Upper Legs"),
    to_UnPool(name="emb15", offset="(5,-6,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Lower Legs"),
    to_UnPool(name="emb16", offset="(5,-10,0)",
              to="(model1-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Whole Body"),

    to_connection("model1-east", "emb11-west"),
    to_connection("model1-east", "emb12-west"),
    to_connection("model1-east", "emb13-west"),
    to_connection("model1-east", "emb14-west"),
    to_connection("model1-east", "emb15-west"),
    to_connection("model1-east", "emb16-west"),

    to_Sum(name="concat1", offset="(10,0,0)", to="(model1-east)", radius=2.5,
           opacity=0.6),

    to_connection("emb11-east", "concat1-west"),
    to_connection("emb12-east", "concat1-west"),
    to_connection("emb13-east", "concat1-west"),
    to_connection("emb14-east", "concat1-west"),
    to_connection("emb15-east", "concat1-west"),
    to_connection("emb16-east", "concat1-west"),

    to_Pool(name="concat1-emb", offset="(3,0,0)",
              to="(concat1-east)", width=2, height=2,
              depth=24, opacity=0.5,
              caption="Concat Feat"),

    to_connection("concat1-east", "concat1-emb-west"),

    to_Pool(name="concat2-emb", offset="(6,0,0)",
              to="(concat1-emb-east)", width=2, height=2,
              depth=24, opacity=0.5,
              caption="Concat Feat"),

    to_connection_double("concat1-emb-east", "concat2-emb-west"),

    to_Sum(name="concat2", offset="(3,0,0)", to="(concat2-emb-east)", radius=2.5,
           opacity=0.6),

    to_connection("concat2-west", "concat2-emb-east"),

    to_UnPool(name="emb21", offset="(5,10,0)",
              to="(concat2-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Head"),
    to_UnPool(name="emb22", offset="(5,6,0)",
              to="(concat2-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Torso"),
    to_UnPool(name="emb23", offset="(5,2,0)",
              to="(concat2-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Arms"),
    to_UnPool(name="emb24", offset="(5,-2,0)",
              to="(concat2-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Upper Legs"),
    to_UnPool(name="emb25", offset="(5,-6,0)",
              to="(concat2-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Lower Legs"),
    to_UnPool(name="emb26", offset="(5,-10,0)",
              to="(concat2-east)", width=2, height=2,
              depth=18, opacity=0.5,
              caption="Whole Body"),

    to_connection("emb21-west", "concat2-east"),
    to_connection("emb22-west", "concat2-east"),
    to_connection("emb23-west", "concat2-east"),
    to_connection("emb24-west", "concat2-east"),
    to_connection("emb25-west", "concat2-east"),
    to_connection("emb26-west", "concat2-east"),

    to_Conv(name='model2', offset="(10,0,0)", to="(concat2-east)",
            width=24, height=16, depth=16, show_labels=False,
            caption='ReID Model'),

    to_connection("model2-west", "emb21-east"),
    to_connection("model2-west", "emb22-east"),
    to_connection("model2-west", "emb23-east"),
    to_connection("model2-west", "emb24-east"),
    to_connection("model2-west", "emb25-east"),
    to_connection("model2-west", "emb26-east"),

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
    
