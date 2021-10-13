1. 

To enable an erase function, you could simply change the color of the mouse to the background color, and also increase the cursor size. 


<!-- inspired from 
    https://www.youtube.com/watch?v=gm1QtePAYTM&ab_channel=TraversyMedia 

    adapted from :

    https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fillText

-->
2. 

To write text, you could use an html form to take input from the user and then give the user other options of customizing the text on the canvas. 

A simple implementation would be changing the font size or color. To actually display the text, you would need to use the Canvas API's module which has a fillText method that can take in text, and a point on canvas.

3.

One way you could do this is that as long as one user is drawing you would halt all other inputs from happening till said person is has finished.

Or similiar to how teams operates, you could the initiator of the whiteboard the admin, and said person could relinquish control to another.
