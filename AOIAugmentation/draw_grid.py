from PIL import Image, ImageDraw

def draw_grids_on_image(image_path, n, m):
    # Load the image
    img = Image.open(image_path)

    # Get image dimensions
    width, height = img.size

    # Calculate grid cell size
    cell_width = width // n
    cell_height = height // m

    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Draw vertical grid lines
    for x in range(0, width, cell_width):
        draw.line([(x, 0), (x, height)], fill=(0, 0, 0), width=1)

    # Draw horizontal grid lines
    for y in range(0, height, cell_height):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0), width=1)

    # Save the modified image
    img.save("grid_image.png")

# Replace "path_to_image.png" with the actual path of your PNG image
# Replace n and m with your desired grid size
draw_grids_on_image("OCT_Image.png", n=50, m=25)

