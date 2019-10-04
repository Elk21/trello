from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from wordcloud import WordCloud
import random


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


def parse_year(year):
    years = year.split('–')
    if len(years) == 1:
        return years[0]
    elif len(years) == 2:
        return f'{years[0]}\n-\n{years[1]}'


def draw_metacritic_rating(user, critic, save_path='img/image.png'):
    img = Image.new('RGB', (768, 120), color=(255, 255, 255))
    fnt = ImageFont.truetype('fonts/CasanovaScotia-Xm0K.ttf', 66)
    d = ImageDraw.Draw(img)
    user_color = rating_color(user.replace('.', ''))
    critic_color = rating_color(critic)

    u_size = fnt.getsize(user)
    c_size = fnt.getsize(critic)

    u_x_offset = (140 - u_size[0]) / 2 + 2
    u_y_offset = (120 - u_size[1]) / 2 - 4
    c_x_offset = (140 - c_size[0]) / 2 + 2 + 140
    c_y_offset = (120 - c_size[1]) / 2 - 4

    d.rectangle([0, 0, 140, 120], fill=user_color)
    d.rectangle([140, 0, 280, 120], fill=critic_color)

    # Left
    d.line([0, 0, 0, 120], fill=black, width=2)
    # Middle
    d.line([140, 0, 140, 120], fill=black, width=2)
    # Right
    d.line([280, 0, 280, 120], fill=black, width=2)
    # Top
    d.line([0, 0, 280, 0], fill=black, width=2)
    # Bottom
    d.line([0, 118, 280, 118], fill=black, width=2)

    d.text((u_x_offset, u_y_offset), text=user, font=fnt, fill=black)
    d.text((c_x_offset, c_y_offset), text=critic, font=fnt, fill=black)

    img.save(save_path)


def draw_word_cloud(text):
    img = Image.open("img/image.png")
    text = {x: random.random() for x in text.split(', ')}

    wordcloud = WordCloud(width=470,
                          height=120,
                          background_color='white',
                          colormap='brg').generate_from_frequencies(text)

    wc = wordcloud.to_image()

    x, y = wc.size
    img.paste(wc, (768-x, 0, 768, y))
    img.save('img/image.png')


def draw_metacritic_image(user, critic, text):
    draw_metacritic_rating(user, critic)
    draw_word_cloud(text)


def draw_imdb_rating(rating, text, year, save_path='img/imdb.png'):
    img = Image.new('RGB', (768, 120), color=(255, 255, 255))
    fnt = ImageFont.truetype('fonts/CasanovaScotia-Xm0K.ttf', 66)
    d = ImageDraw.Draw(img)
    rate_color = rating_color(rating.replace('.', ''))

    rating_size = fnt.getsize(rating)

    u_x_offset = (140 - rating_size[0]) / 2 + 2
    u_y_offset = (120 - rating_size[1]) / 2 - 4

    d.rectangle([0, 0, 140, 120], fill=rate_color)
    # Left
    d.line([0, 0, 0, 120], fill=black, width=2)
    # Middle
    d.line([140, 0, 140, 120], fill=black, width=2)
    # Right
    d.line([280, 0, 280, 120], fill=black, width=2)
    # Top
    d.line([0, 0, 280, 0], fill=black, width=2)
    # Bottom
    d.line([0, 118, 280, 118], fill=black, width=2)

    d.text((u_x_offset, u_y_offset), text=rating, font=fnt, fill=black)

    # Create image with year
    fnt = ImageFont.truetype('fonts/CasanovaScotia-Xm0K.ttf', 32)
    year = parse_year(year)

    if '-' in year:
        one = fnt.getsize('0000')
        two = fnt.getsize('-')
        year_size = (one[0], one[1] * 2 + two[1])
    else:
        year_size = fnt.getsize(year)

    y_x_offset = (140 - year_size[0]) / 2 + 2 + 140
    y_y_offset = (120 - year_size[1]) / 2 - 4

    d.text((y_x_offset, y_y_offset), text=year, font=fnt, fill=black)

    text = {x: random.random() for x in text.split(', ')}

    # Create image with genres word cloud
    wordcloud = WordCloud(width=470,
                          height=120,
                          background_color='white',
                          colormap='brg').generate_from_frequencies(text)

    wc = wordcloud.to_image()
    x, y = wc.size
    img.paste(wc, (768-x, 0, 768, y))

    img.save(save_path)


# draw_metacritic_image('5.3', '83', 'Action, Shooter, First-Person, Arcade')
draw_imdb_rating('8.3', 'Drama, Mystery, Sci-Fi, Thriller', '2015–2018')
