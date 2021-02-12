from pitwi import *

(
    Root(width = 45, height = 8)
    .add(Text('Puf', bg='white', fg='black'))
    .add(Text('Paf'), row=2, column=2)
    .run()
)