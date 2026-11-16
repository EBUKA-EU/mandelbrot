import tkinter as tk

def create_window():
   """Create a Tkinter window with a Canvas for graphics."""
   root = tk.Tk()
   root.title("Mandelbrot Explorer")

   # Create a 500 x 500 Canvas with a white background.
   canvas = tk.Canvas(root, width=500, height=500, bg="white")
   # Add the canvas to the window
   canvas.pack()
   canvas.create_rectangle(100,100,300,300, fill="blue")
   # Keeps the application running and processe user events
   root.mainloop()

def draw_pixel_image():
   """ Create a Tkinter window displaying a two-color pixel image"""
   root = tk.Tk()
   root.title("Pixel Drawing Practice")

   #Create a 100 x 100 Canvas and pack it
   canvas = tk.Canvas(root, width=100, height=100, bg="white")
   canvas.pack()

   # Create a 100 x 100 PhotoImage
   image = tk.PhotoImage(width=100, height=100)

   # Use nested loops to visit each pixel
   for y in range(100):
      for x in range(100):
         if y < 50:
            image.put("blue", to=(x, y))
         else:
            image.put("orange", to=(x, y))

   # Display the PhotoImage on the Canvas
   canvas.create_image(0,0,image=image, anchor="nw")
   # Keep a reference to the image
   canvas.image = image

   root.mainloop()


if __name__ == "__main__":
  create_window()

if __name__ == "__main__":
   draw_pixel_image()
