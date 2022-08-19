# Color_Palette  
  
[!image](https://i.imgur.com/wzgRGBx.jpg)
  
# About  
  
## Goal  
This app is supposed to be a small tool for artists and designers. When working inside graphics editing programs I've often catched myself switching back and forth between the editor and google in search of colors and shades. This becomes even messier when, like me, a person has 2 screens with one reserved for the editor and the second one for reference images. This app delivers the possibility to declutter the working space and give all-in-one tool pack just in reach of your mouse cursor.  
  
And so this app comes into play. It allows you to pick color and get the HEX or RGB value of it, see different color shades and create and save custom color palettes, all while this program stays on top of other software so you don't have to switch between windows (which can get very confusing with bigger projects where you have tons of windows).  
This program also allows you for quick export of the saved color palettes as .jpegs, which then you can load into editor and copy colors from. You can also generate color palette from a image, like drawing or photo or simply another color palette. If you see a color/shade you like, you can also copy it via eyedropper tool, from any website or app or image and add it to the palette or get it's HEX value.  
  
## Problems and lessons  
Because I'm working with Tkitner, which is a very outdated GUI module, a lot of sacrifices and compromises had to be made. I've had to make few workarounds and 'brute methods' that might confuse users at first but nonetheless I've managed to avoid removing entire features or making this app something less than it's supposed to be.  
  
I can say that this project increased my GUI skills. I've aimed to make the UI look fairly modern, and considering that I was using such an old system like Tkinter, I'd say I did pretty good. The beauty-ness of the design lies in it's simplicity.  
  
Another valuable experience was working with save files, I never tried anything related to saving informatiom between sessions so I had to think it out properly. I had a lot of different ideas but in the end I've sticked to the classic .txt file extension that simply contained Python lists ready to be imported into the program. A upside of this crude mechanic is that users can edit palettes manually inside the .txt file, this makes a lot of things easier and more comfortable for users.  
  
TO-DO:    
[ ] Add option for the app to always stay on top of other programs  
[ ] Save color palettes to a file  
[ ] Generate color shades when picking a color  
[ ] Generate color palette from uploaded image  
[ ] Copy color from any website, app or image via eyedropper tool  
[ ] Generate random colors or color palettes  
[ ] Export color palettes as .jpegs, for use in image editing software  
[ ] REDO / UNDO options  
  
# License  
GNU GENERAL PUBLIC LICENSE  
  
Made by Adrian Urbaniak, 2022
