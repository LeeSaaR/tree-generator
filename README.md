# TreeGenerator

(This project will not be developed further.)

**TreeGenerator** is a Blender Add-on that generates simple trees.

Make a tree in 3 Steps:
+ Generate stem
+ Generate branches
+ Add twigs to the branches

*** 
### Dependencies
Blender 2.80 or greater ( Tested on 3.6 )

*** 
### Installation
Install like any other Blender Add-on:  
+ Download the zip file 
+ Open Blender
+ Go to: `Edit > Preferences > Add-ons`
+ Click `Install...`
+ Choose the downloaded zip file
+ Click `Install Add-on`
+ Activate Add-on

***
### Location
_LSR Tree_ is located at:  
`3D View (N-Panel)  > LSR > Tree`  

There are 3 Sub Panels:
+ Stem
+ Branches
+ Twigs

***
### Generate a tree using LSR Tree:

#### Start LSR Tree

Click on:  
`3D View (N-Panel)  > LSR > Tree > enable`

This creates multiple Collections for the LSR Tree Output:
+ LSR_TREE_STEM
+ LSR_TREE_BRANCHES
+ LSR_TREE_TWIGS
+ LSR_TREE_OUT
+ LSR_TREE_META  
  
> Do not rename these collections!

Now the Stem Panel is active.

***
#### Stem Panel
  
###### Parameters:
+ **height** - height of the stem 
+ **segments** - segments count of the stem curve 
+ **base radius** - radius of the stem's base 
+ **min radius** - min radius of the stem's tip  
+ **straightness** - controls the straightness of the stem 

When you click on:   
`3D View (N-Panel)  > LSR > Tree > Stem > add`  
the stem is generated.

You can always click on:  
`3D View (N-Panel)  > LSR > Tree > reset stem`  
to reset the stem. Play around with the parameters!

At this stage you can also go into Edit Mode and adjust the Bezier Curve to your needs.  
When you're happy with the result of the stem generation stage move to the Branches Panel.

***
#### Branches Panel

###### Parameters:
+ **count** - branch count
+ **segment** - segment count of each branch
+ **straightness** - straightness of the branches 
+ **start height** - start height of the branches
+ **start angle** - start angle of the branches  
+ **end angle** - end angle of the branches 
+ **z-rotation** - z rotation offset
+ **width** - width of branches 
+ **over top** - branch over top stem

Click on:   
`3D View (N-Panel)  > LSR > Tree > Branches > add`  
to add the branches.

Click on:  
`3D View (N-Panel)  > LSR > Tree > reset branches`  
to reset the branches. Play around with the parameters!

If you are happy with the results, click on:  
`3D View (N-Panel)  > LSR > Tree > Branches > convert to mesh`

This will convert the Stem and Branch Curves to Meshes and uv unwraps them.

Now the Twig Panel is active.

***
#### Twigs Panel
> LSR Tree is designed to use Twig Objects as Planes with Alpha Images on it, so LSR tree does not generate Twig Objects by itself. It uses a Collection of Twig Object you define. It is not mandatory to use Plane Objects as Twigs, but it is recommended.

First you need to setup a Twig Collection. Be sure that the Twig Objects are pointing upwards on the z-axis. This assures that the twigs are placed on the branches properly. 

Now Select your Twig Collection in the Twig Panel.

###### Parameters:
+ **start angle** - start angle of twigs
+ **end angle** - end angle of twigs  
+ **start** - polygons where the twigs start
+ **end** - polygons where the twigs end
