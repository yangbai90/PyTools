from PIL import Image


nfigs=601

def append_images(images, direction='horizontal',
                  bg_color=(255,255,255), aligment='center'):
    """
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: white)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """
    widths, heights = zip(*(i.size for i in images))

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)

    new_im = Image.new('RGB', (new_width, new_height), color=bg_color)


    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im

for i in range(nfigs):
    str='co.%04d.jpeg'%(i);img1=Image.open(str)
    str='stress.%04d.jpeg'%(i);img2=Image.open(str)
    str='iron.%04d.jpeg'%(i);img3=Image.open(str)
    str='h2.%04d.jpeg'%(i);img4=Image.open(str)
    pic1 = append_images([img1, img2], direction='horizontal')
    pic2 = append_images([img3, img4], direction='horizontal')
    final = append_images([pic1, pic2], direction='vertical')
    str='Combine-%04d.jpeg'%(i)
    final.save(str)
