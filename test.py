from PIL import Image, ImageDraw, ImageFont, ImageEnhance

user = '81'
critic = '11'
green = (0, 175, 0)
yellow = (230, 230, 0)
red = (210, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)


def rating_color(n):
    n = int(n)

    if n < 49:
        return red
    elif n < 74:
        return yellow
    else:
        return green


def draw_metacritic_rating(user, critic):
    img = Image.new('RGB', (800, 120), color=(255, 255, 255))
    fnt = ImageFont.truetype('fonts/CasanovaScotia-Xm0K.ttf', 66)
    d = ImageDraw.Draw(img)
    user_color = rating_color(user.replace('.', ''))
    critic_color = rating_color(critic)

    u_size = fnt.getsize(user)
    c_size = fnt.getsize(critic)

    u_x_offset = (120 - u_size[0]) / 2 + 2
    u_y_offset = (120 - u_size[1]) / 2 - 4
    c_x_offset = (120 - c_size[0]) / 2 + 2 + 120
    c_y_offset = (120 - c_size[1]) / 2 - 4

    d.ellipse([4, 4, 116, 116], fill=user_color)
    d.ellipse([124, 4, 236, 116], fill=critic_color)

    d.text((u_x_offset, u_y_offset), text=user, font=fnt, fill=black)
    d.text((c_x_offset, c_y_offset), text=critic, font=fnt, fill=black)

    encancer = ImageEnhance.Sharpness(img)

    img = encancer.enhance(0.0)

    img.save('img/pil_text_font.png')
